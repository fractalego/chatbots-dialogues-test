import nltk
import random
import igraph as ig
import matplotlib.pyplot as plt

from gensim.models import Doc2Vec
from gensim import utils

from plot_chat_path import plot_sentiment, plot_temporal_cluster_using_path, load_tsne_coordinates_from


class ConversationGraph:
    def __init__(self, conversation_file, edges_filename, doc2vec_filename):
        self.g, self.vertex_to_lines_dict, self.lines_to_vertex_dict = self._load_edges(edges_filename)
        self.doc2vec_model = Doc2Vec.load(doc2vec_filename)
        self.goal_line = 'LINES_106702'
        self.goal = self.lines_to_vertex_dict[self.goal_line]
        self.goal_vector = self.doc2vec_model.docvecs[self.goal_line]
        self.lines_dict = {'LINES_' + str(i): line.replace('\n', '')
                           for i, line in enumerate(open(conversation_file,
                                                         encoding="ISO-8859-1").readlines())}
        self.current_node = -1
        self.current_vector = []
        self.path = []
        self.lines_in_path = []

    def _load_edges(self, filename):
        file = open(filename)
        lines = file.readlines()
        g = ig.Graph(directed=False)

        vertex_to_lines_dict = {}
        lines_to_vertex_dict = {}
        vertices = set()
        edges = []
        for line in lines:
            row = line.split(';')
            weight = row[4]
            if int(weight) < 2:
                continue
            from_vertex = row[0]
            to_vertex = row[2]
            from_lines = row[1].replace(' ', '').replace('\'', '').split(',')
            to_lines = row[3].replace(' ', '').replace('\'', '').split(',')
            vertex_to_lines_dict[from_vertex] = from_lines
            vertex_to_lines_dict[to_vertex] = to_lines
            for line in from_lines:
                try:
                    lines_to_vertex_dict[line].append(from_vertex)
                except:
                    lines_to_vertex_dict[line] = from_vertex
            for line in to_lines:
                try:
                    lines_to_vertex_dict[line].append(to_vertex)
                except:
                    lines_to_vertex_dict[line] = to_vertex
            vertices.add(from_vertex)
            vertices.add(to_vertex)
            edges.append((from_vertex, to_vertex))
        g.add_vertices(list(vertices))
        g.add_edges(edges)
        return g, vertex_to_lines_dict, lines_to_vertex_dict

    def _get_most_similar_vertex_from_string(self, string):
        model = self.doc2vec_model
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(utils.to_unicode(string))
        words = [word.lower() for word in words]
        vector = model.infer_vector(words)
        pairs = model.docvecs.most_similar([vector], topn=1000)
        best_node = -1
        best_vector = ''
        best_line = ''
        for pair in pairs:
            line = pair[0]
            try:
                vertex = self.lines_to_vertex_dict[line]
                best_node = vertex
                best_vector = model.docvecs[line]
                best_line = line
                break
            except:
                pass
        return best_node, best_vector, best_line

    def define_endpoint(self, end_string):
        self.goal, self.goal_vector, _ = self._get_most_similar_vertex_from_string(end_string)

    def _get_shortest_paths(self, start, end):
        try:
            position = self.path.index(int(start))
            self.path = self.path[position + 1:]
            return self.path
        except:
            pass
        self.path = self.g.get_shortest_paths(start, end)[0]
        return self.path

    def _find_next_node_in_path(self, node):
        path = self._get_shortest_paths(node, self.goal)
        if path:
            return str(path[0])
        return -1

    def _find_random_line_number_in_node(self, node):
        lines_in_node = self.vertex_to_lines_dict[node]
        return random.choice(lines_in_node)

    def find_next_line_in_path(self, string):
        current_node, current_vector, current_line = self._get_most_similar_vertex_from_string(string)
        if not self.lines_in_path:
            self.lines_in_path.append(current_line)
        if current_node == self.goal:
            return 'END!'
        node = self._find_next_node_in_path(current_node)
        if node == self.goal:
            return 'END!'
        if node == -1:
            node = self.goal
        self.current_node = node
        self.current_vector = current_vector
        chosen_line_number = self._find_random_line_number_in_node(node)
        chosen_line = self.lines_dict[chosen_line_number]
        self.lines_in_path.append(chosen_line_number)
        return chosen_line

    def get_line_numbers_in_path(self):
        return [int(item.replace('LINES_', '')) for item in self.lines_in_path]

    def start_new_path(self):
        self.lines_in_path = []


if __name__ == '__main__':

    conversation_graph = ConversationGraph('ordered_lines.txt',
                                           'results/edges.txt',
                                           'lines-150.d2v')
    FIRST_LINE = 'Hello! How are you?'
    LAST_LINE = 'Goodbye!'
    conversation_graph.define_endpoint(LAST_LINE)
    line_xy_dict, _ = load_tsne_coordinates_from('results/tsne_coordinates.txt')

    for _ in range(100):
        lines = []
        conversation_graph.start_new_path()
        next_line = FIRST_LINE
        while next_line != 'END!':
            print('Alice: ', next_line)
            next_line = conversation_graph.find_next_line_in_path(next_line)
            if next_line == 'END!':
                print('Bob:', LAST_LINE)
                break

            print('Bob:', next_line)
            next_line = conversation_graph.find_next_line_in_path(next_line)
            if next_line == 'END!':
                print('Alice:', LAST_LINE)
                break
            print('')
        nodes_in_path = conversation_graph.get_line_numbers_in_path()
        plot_sentiment(line_xy_dict)
        plot_temporal_cluster_using_path(line_xy_dict, nodes_in_path)
        plt.show()
        print('--')
