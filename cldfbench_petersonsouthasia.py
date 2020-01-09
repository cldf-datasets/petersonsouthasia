import pathlib
import itertools
import collections

from cldfbench import Dataset as BaseDataset
from cldfbench import CLDFSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "petersonsouthasia"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module='StructureDataset')

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component('LanguageTable')
        args.writer.cldf.add_component('ParameterTable')
        args.writer.cldf.add_component('CodeTable')
        args.writer.cldf['ValueTable', 'Value'].null = ['?']

        codes = collections.OrderedDict()
        for (fid, fname), rows in itertools.groupby(
            self.raw_dir.read_csv('codes.csv', dicts=True),
            lambda r: (r['Parameter_ID'], r['Parameter_Name'])
        ):
            codes[fid] = (fname, list(rows))
            for row in codes[fid][1]:
                args.writer.objects['CodeTable'].append({
                    'ID': '{0}-{1}'.format(row['Parameter_ID'], row['Number']),
                    'Parameter_ID': row['Parameter_ID'],
                    'Name': row['Number'],
                    'Description': row['Description'],
                })

        for l in self.etc_dir.read_csv('languages.csv', dicts=True):
            args.writer.objects['LanguageTable'].append(l)

        for i, row in enumerate(self.raw_dir.read_csv('Tabelle1.csv', dicts=True)):
            if i == 0:
                for j, name in enumerate(row.keys()):
                    if j > 0:
                        if "'" in name and not name.startswith("'"):
                            name = "'" + name
                        fid, (desc, _) = list(codes.items())[j - 1]
                        args.writer.objects['ParameterTable'].append({
                            'ID': fid,
                            'Name': name,
                            'Description': desc,
                        })
            lid = None
            for j, v in enumerate(row.values()):
                if j == 0:
                    lid = v
                else:
                    pid = list(codes.keys())[j - 1]
                    args.writer.objects['ValueTable'].append({
                        'ID': '{0}-{1}'.format(lid, str(j)),
                        'Language_ID': lid,
                        'Parameter_ID': pid,
                        'Value': v,
                        'Code_ID': '{0}-{1}'.format(pid, v) if v != '?' else None,
                    })
