import csv
import geocoder

path_to_csv = input('Enter the path to *.csv with locations names to geocode: ')
path_for_output = input('Enter the path to save output geocoded csv: ')

def open_csv_as_list(path_to_csv):
    users = []
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)
        pages_list = list(reader)
    for p in pages_list:
        user = p[0]
        users.append(user)
    return users


def save_list_as_scv(output_path, list, encoding='utf-8'):
    with open(output_path, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in list:
            try:
                writer.writerow([val])
            except UnicodeEncodeError as err:
                print('Decoding this shit' + str(err))
                try:
                    val = val.encode('cp1251').decode('utf-8')
                    writer.writerow([val])
                except:
                    pass; writer.writerow(['undefined'])


lis = open_csv_as_list(path_to_csv)

users_geo = []

for l in lis:
    geo = geocoder.arcgis(str(l)).latlng
    users_geo.append(geo)
    print(geo)
    save_list_as_scv(path_for_output, users_geo)

save_list_as_scv(path_for_output, users_geo)

print('Finished!')
