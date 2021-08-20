from pathlib import Path
import json

index_html = Path(__file__).with_name('index.template').open('r').read()
t_album = Path(__file__).with_name('album.template').open('r').read()

albums = {}

for album in Path(__file__).parent.with_name('models').iterdir():
    album_name = int(album.name.split('_')[0])
    albums[album_name] = {
        'path': album.name,
        'images': []
    }
    for image in Path(album).glob('*.jpg'):
        if image.name != 'cover.jpg':
            albums[album_name]['images'].append(image.name)
    for content in Path(album).glob('content.json'):
        albums[album_name]['content'] = json.load(content.open())

album_i = 0
index_image_html = ''

for album_num in reversed(sorted(list(albums.keys()))):
    album = albums[album_num]
    album_html = t_album
    album_html = album_html.replace('$$title$$', album['content']['title'])
    album_html = album_html.replace('$$description$$', album['content']['description'])

    if album_i%4 == 0:
        index_image_html += '\t\t<div class="w3-row-padding">\n'
    index_image_html += ('\t\t\t<div class="w3-quarter">\n'
                         '\t\t\t\t<div class="w3-card w3-hover-shadow">\n'
                         '\t\t\t\t\t<a href="models/' + album['path'] + '/album.html">\n'
                         '\t\t\t\t\t\t<img src="models/' + album['path'] + '/cover.jpg" '
                         'class="w3-image w3-round" alt="' + album['content']['title'] + '">\n'
                         '\t\t\t\t\t\t<div class="w3-container w3-center">\n'
                         '\t\t\t\t\t\t\t<p>' + album['content']['title'] + '</p>\n'
                         '\t\t\t\t\t\t</div>\n'
                         '\t\t\t\t\t</a>\n'
                         '\t\t\t\t</div>\n'
			             '\t\t\t</div>\n')
    if album_i%4 == 3 or album_i == len(albums)-1:
        index_image_html += '\t\t</div>'
    album_i += 1
    
    col_1_html=''
    col_2_html=''
    col_3_html=''
    for i in range(len(album['images'])):
        image_html = '\t\t\t\t<img src="' + album['images'][i] + '" class="w3-margin-bottom w3-image w3-round">\n'
        col = album['images'][i].split('_')[0]
        if col == '1':
            col_1_html += image_html
        elif col == '2':
            col_2_html += image_html
        else:
            col_3_html += image_html
    
    album_html = album_html.replace('$$col_1$$', col_1_html)
    album_html = album_html.replace('$$col_2$$', col_2_html)
    album_html = album_html.replace('$$col_3$$', col_3_html)

    p = Path(__file__).parent.parent / 'models' / album['path'] / 'album.html'
    if p.is_file():
        p.unlink()
    p.touch()
    p.write_text(album_html)

index_html = index_html.replace('$$index_image$$', index_image_html)

p = Path(__file__).parent.parent / 'index.html'
if p.is_file():
    p.unlink()
p.touch()
p.write_text(index_html)