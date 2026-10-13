#!/usr/bin/env python3
"""Read the pinned Chaldea snapshot without network access or dependencies."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'data' / 'chaldea'

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def expand_function(ref, functions):
    result = deepcopy(functions[ref['funcId']])
    result.update(deepcopy(ref))
    first = result.get('svals', [{}])[0]
    for key in ('svals', 'svals2', 'svals3', 'svals4', 'svals5'):
        if key in result:
            result[key] = [deepcopy(first) | value for value in result[key]]
    return result

def expand_skill(ref, bases, functions):
    result = deepcopy(bases[ref['id']])
    result.update(deepcopy(ref))
    result['functions'] = [expand_function(f, functions) for f in result.get('functions', [])]
    return result

def latest_skills(servant):
    best = {}
    for ref in servant['skills']:
        slot = ref['num']
        if slot not in best or ref.get('priority', 1) > best[slot].get('priority', 1):
            best[slot] = ref
    return [best[n] for n in sorted(best)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', help='Servant ID or name fragment (Japanese/Chinese/English)')
    parser.add_argument('--full', action='store_true', help='Expand latest-priority skills and all NP versions')
    parser.add_argument('--all-skills', action='store_true', help='With --full, include older skill versions')
    args = parser.parse_args()
    servants = [s for p in sorted(ROOT.glob('servants.*.json')) for s in json.loads(p.read_text())]
    names = read('mappingData.3.json')['svt_names']
    matches = []
    for servant in servants:
        translations = names.get(servant['name'], {})
        labels = [servant['name'], *[v for v in translations.values() if isinstance(v, str)]]
        if args.query == str(servant['id']) or any(args.query.casefold() in label.casefold() for label in labels):
            matches.append((servant, translations))
    if not matches:
        parser.exit(1, 'No matching servant in this snapshot.\n')
    if args.full:
        skills = {x['id']: x for x in read('baseSkills.json')}
        tds = {x['id']: x for x in read('baseTds.json')}
        functions = {x['funcId']: x for x in read('baseFunctions.json')}
        output = []
        for servant, translations in matches:
            result = deepcopy(servant)
            result['translatedNames'] = translations
            refs = servant['skills'] if args.all_skills else latest_skills(servant)
            result['skills'] = [expand_skill(ref, skills, functions) for ref in refs]
            result['noblePhantasms'] = [expand_skill(ref, tds, functions) for ref in servant.get('noblePhantasms', [])]
            output.append(result)
    else:
        output = [{'id': s['id'], 'collectionNo': s['collectionNo'], 'name': s['name'],
                   'translatedNames': t, 'classId': s['classId'], 'rarity': s['rarity']}
                  for s, t in matches]
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
