from pymongo import MongoClient

def get_file_path():
    '''
    Take file path of the .zarr file. Ignore hashtagged items.
    '''

    file_path = ''
    
    # Skips the first line so that the following loop does not break
    input()

    while True:
        file_path = input()

        if file_path.startswith('#'):
            continue
        
        elif file_path.startswith('~') or file_path.startswith('/'):
            statement.append(file_path)
        
        elif file_path.startswith('--'):
            break
    
    statement.append('-d')

def get_layers(dataset_path: str):
    '''
    ### Parameters
    dataset_path: the file path the layer within the .zarr file where all the data is from
    '''

    global statement
    global layer

    while True:
        layer = input()

        if layer.startswith('#'):
            continue
        
        if layer.startswith('--'):
            break

        layer = layer.split('--')[0].strip()

        # Bounds numbers found, add multiple
        if '-' in layer:
            data = layer.split(' ')
            prefix = data[0]
            s_e = data[1].split('-')
            start = int(s_e[0])
            end   = int(s_e[1]) + 1
            for i in range(start, end):
                statement.append(dataset_path + prefix + str(i))    
        else:
            statement.append(dataset_path + layer)

def get_pred_layer():
    '''
    Take input from the user for the training and prediction run IDs. Then append both of these in specified format to the statement.
    '''

    global statement

    pred_ids = []

    while True:
        pred_id = input()

        if pred_id.startswith('#'):
            continue

        if pred_id.startswith('--'):
            break

        # Take the number portion of the prediction id, not the 
        pred_id = pred_id.split('--')[0].strip()

        pred_ids.append(pred_id)
        
    # Connect to MongoDB to query training run id    
    client = MongoClient('tkv8', 27017)
    db = client.fiborganelle_predictions
    
    for pred_id in pred_ids:
        entry = db.runs.find_one({ "_id": int(pred_id)})

        train_id = entry['config']['prediction']['run_id_training']

        statement.append(f'volumes/predictions/train_{train_id}/predict_{pred_id}/segmentation')

if __name__ == '__main__':
    statement = ['neuroglancer', '-f']

    get_file_path()

    layer = ''

    # Add raw layers
    get_layers('volumes/')

    # Add label layers
    get_layers('volumes/labels/')

    # Add prediction layers
    get_pred_layer()

    # Misc Layers
    get_layers('')

    # Add bounds
    get_layers('bounds/')

    # Serve to other machines on network
    # statement.append('--serve')
    
    print(' '.join(statement), end='')
