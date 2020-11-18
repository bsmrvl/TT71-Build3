import pandas as pd
import json
from kickstarter_app import DB, Record

def go():
    df = pd.read_csv('data/KS_US_latest_10k_finished.csv', dtype=object)
    DB.drop_all()
    DB.create_all()
    for i in range (df.shape[0]):
        record = Record()
        record.id = i
        record.name = df.iloc[i]['name']
        record.blurb = df.iloc[i]['blurb']
        record.link = json.loads(df.iloc[i]['urls'])['web']['project']
        record.category_name = json.loads(df.iloc[i]['category'])['name']
        record.launch_timestamp = df.iloc[i]['launched_at']
        record.deadline_timestamp = df.iloc[i]['deadline']
        record.pledged = df.iloc[i]['pledged']
        record.goal = df.iloc[i]['goal']
        record.location = json.loads(df.iloc[i]['location'])['short_name']
        DB.session.add(record)
        if i%1000 == 0:
            print(f'{i} done...')
    print('all done.')
    DB.session.commit()
    return('done')

if __name__ == '__main__':
    go()