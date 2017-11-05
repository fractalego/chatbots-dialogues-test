import matplotlib.pyplot as plt


def load_tsne_coordinates_from(filename):
    file = open(filename)
    lines = file.readlines()
    line_xy_dict = {}
    line_to_xy_dict = {}
    for line in lines:
        row = line.split()
        x = float(row[0])
        y = float(row[1])
        try:
            line_id = row[2]
        except:
            continue
        line_xy_dict[line_id] = (x, y)
        line_to_xy_dict[(x, y)] = line_id
    return line_xy_dict, line_to_xy_dict

def plot_sentiment(line_xy_dict):
    xs = []
    ys = []
    for key, (x, y) in line_xy_dict.items():
        xs.append(x)
        ys.append(y)
    plt.scatter(xs, ys, marker='.', c='r', s=1.3, linewidth=0)
    plt.legend(loc='best')


def plot_temporal_cluster(line_xy_dict, start, end):
    sequence_x = []
    sequence_y = []
    sequence_labels_dict = {}
    index = 0
    for line_id in range(start, end):
        line_str = 'LINES_' + str(line_id)
        x, y = line_xy_dict[line_str]
        index += 1
        sequence_x.append(x)
        sequence_y.append(y)
        sequence_labels_dict[str(index)] = (x, y)
    for key in sequence_labels_dict.keys():
        plt.annotate(key, xy=sequence_labels_dict[key], fontsize=30)
    plt.plot(sequence_x, sequence_y, marker='.', color='k', )


def plot_temporal_cluster_using_path(line_xy_dict, path):
    sequence_x = []
    sequence_y = []
    sequence_labels_dict = {}
    index = 0
    for line_id in path:
        line_str = 'LINES_' + str(line_id)
        x, y = line_xy_dict[line_str]
        index += 1
        sequence_x.append(x)
        sequence_y.append(y)
        sequence_labels_dict[str(index)] = (x, y)
    for key in sequence_labels_dict.keys():
        plt.annotate(key, xy=sequence_labels_dict[key], fontsize=30)
    plt.plot(sequence_x, sequence_y, marker='.', color='k', )
