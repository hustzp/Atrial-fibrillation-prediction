
import numpy as np
import os


class FileExtract:
    def extract(self, path, file, interval=90):
        '''
            :param path: test path
            :param file: file to process
            :param interval: sample length
            :return: test samples
        '''

        file_path = path + '/' + file
        assert os.path.exists(file_path)

        with open(file_path) as f:
            data = f.readlines()

        if 'PAF' not in path:
            self._load_test_data(data, interval)
        else:
            self._load_test_data_2(data, interval)

        return self.test_x

    def _load_test_data(self, data, interval):
        seq = np.asarray([line.strip().split(' ')[0][1:] for line in data], dtype=np.int64)
        t_list = np.asarray([line.strip().split(' ')[0][0] for line in data])
        seq[t_list == 'Z'] = 0
        # seq[t_list == 'A'] = 0
        # seq[t_list == 'V'] = 0

        self.test_x = np.reshape(seq[:seq.shape[0]//interval*interval], (-1, interval))
        self.test_x = self.test_x[(self.test_x > 0).all(axis=-1)]

    def _load_test_data_2(self, data, interval):
        self._get_start_time(data)
        self.label = []
        self._get_label(data)

        i = 0
        for line in data:
            i += 1
            if line.strip() == 'End header':
                break

        total_time = np.asarray([int(line[1:3]) * 3600 + int(line[4:6]) * 60 + int(line[7:9])
                                 for line in data[i:]])
        total_time[total_time < self.start_time] += 24 * 3600
        seq = np.asarray([line.strip().split(' ')[0].split(']')[-1][1:]
                          if len(line.strip().split(' ')[0].split(']')[-1]) > 0 else 0
                          for line in data[i:]], dtype=int)
        t_list = np.asarray([line.strip().split(' ')[0].split(']')[-1][0]
                             if len(line.strip().split(' ')[0].split(']')[-1]) > 0 else 'Z'
                             for line in data[i:]])

        label_seq = np.zeros_like(seq)
        label_seq[t_list == 'Z'] = -1
        # label_seq[t_list == 'A'] = -1
        # label_seq[t_list == 'V'] = -1

        for each in self.label:
            label_seq[(total_time >= each[0]) & (total_time <= each[1])] = 1

        self.test_x = np.reshape(seq[:seq.shape[0]//interval*interval], (-1, interval))
        test_y = np.reshape(label_seq[:label_seq.shape[0]//interval*interval], (-1, interval))
        self.test_x = self.test_x[(test_y == 0).all(axis=-1)]

    def _get_start_time(self, data):
        for index, line in enumerate(data):
            if line.startswith('Start time'):
                line = line.split(':')
                self.start_time = int(line[1]) * 3600 + int(line[2]) * 60
                return

    def _get_label(self, data):
        i = 4
        while data[i][:2] != 'RR' and data[i] != '\n':
            cur = data[i].strip()
            if cur[-1] == '0' or cur[-1] == ')':
                time1 = int(cur[:2]) * 3600 + int(cur[3:5]) * 60 + int(cur[6:8])
                second = int(cur.split('(')[-1].split(')')[0])
                if time1 < self.start_time:
                    time1 += 24 * 3600
                self.label.append([time1, time1+second])
            i += 1


if __name__ == '__main__':
    data_path = '../data/PAF'
    file_extract = FileExtract()

    files = os.listdir(data_path)
    x = file_extract.extract(data_path, files[0], 90)

    print(x.shape)
