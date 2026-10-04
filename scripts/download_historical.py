"""Download public community uploads; extract only replay files, never executables."""
import requests, json, zipfile, io, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for ident in [110,147,119,159]:
 url=f'https://uu.getuploader.com/toric/download/{ident}'
 session=requests.Session();r=session.get(url,timeout=30)
 soup=BeautifulSoup(r.text,'html.parser');form=soup.find('form',method='POST')
 values={i.get('name'):i.get('value','') for i in form.find_all('input') if i.get('name')}
 response=session.post(url,data=values,timeout=30)
 ROOT.joinpath('sources',f'uploader-{ident}-after.html').write_text(response.text if not response.content.startswith(b'PK') else 'binary ZIP response')
 if not response.content.startswith(b'PK'):
  soup=BeautifulSoup(response.text,'html.parser')
  links=[a.get('href') for a in soup.find_all('a',href=True) if a['href'].startswith('https://downloadx.getuploader.com/')]
  print(ident,'status',response.status_code,'binary',False,'download links',len(links))
  if links: response=session.get(links[0],timeout=45)
 row=dict(id=ident,source_url=url,status=response.status_code,bytes=len(response.content),downloaded=False)
 if response.content.startswith(b'PK') and len(response.content)<50_000_000:
  path=ROOT/'raw'/f'historical_{ident}.zip';path.write_bytes(response.content)
  directory=ROOT/'raw'/f'historical_{ident}';directory.mkdir(exist_ok=True)
  names=[]
  with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
   for item in archive.infolist():
    if item.file_size<50_000_000 and Path(item.filename).suffix.lower() in ['.mgz','.mgx','.mgx2','.aoe2record']:
     dest=directory/Path(item.filename).name;dest.write_bytes(archive.read(item));names.append(dest.name)
  row.update(downloaded=True,sha256=hashlib.sha256(response.content).hexdigest(),recordings=names)
 print(ident,row['downloaded'],row['bytes'],len(row.get('recordings',[])))
 rows.append(row)
ROOT.joinpath('sources','historical-downloads.json').write_text(json.dumps(rows,indent=2))
