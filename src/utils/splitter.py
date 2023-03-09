import os
import shutil


class Splitter:
    def __init__(self, input_path, balance: bool):
        self.accepted_path = os.path.join(input_path, "accepted")
        self.rejected_path = os.path.join(input_path, "rejected")
        self.root_path = os.path.join(input_path, "..", "..")

        self.train_path = os.path.join(self.root_path, "dist", "train")
        self.valid_path = os.path.join(self.root_path, "dist", "valid")
        self.test_path = os.path.join(self.root_path, "dist", "test")

        if not balance:
            self.train_path = os.path.join(self.root_path, "dist-unbalanced", "train")
            self.valid_path = os.path.join(self.root_path, "dist-unbalanced", "valid")
            self.test_path = os.path.join(self.root_path, "dist-unbalanced", "test")

        self.train_accepted_path = os.path.join(self.train_path, "accepted")
        self.train_rejected_path = os.path.join(self.train_path, "rejected")

        self.valid_accepted_path = os.path.join(self.valid_path, "accepted")
        self.valid_rejected_path = os.path.join(self.valid_path, "rejected")

        self.accepted_list = os.listdir(self.accepted_path)
        self.accepted_list_len = len(self.accepted_list)

        self.rejected_list = os.listdir(self.rejected_path)
        self.rejected_list_len = len(self.rejected_list)

        self.valid_test_len = round(self.rejected_list_len * 0.1)
        self.train_len = round(self.rejected_list_len * 0.8)
        if not balance:
            self.train_len = round(self.accepted_list_len * 0.8)

        os.makedirs(self.train_accepted_path)
        os.makedirs(self.train_rejected_path)
        os.makedirs(self.valid_accepted_path)
        os.makedirs(self.valid_rejected_path)
        os.makedirs(self.test_path)

    def __valid_split(self):
        accepted_list = os.listdir(self.accepted_path)
        rejected_list = os.listdir(self.rejected_path)

        for i in range(self.valid_test_len):
            file_full_path = os.path.join(self.accepted_path, accepted_list[i])
            shutil.move(file_full_path, self.valid_accepted_path)
        print(f"{self.valid_test_len} images moved to {self.valid_accepted_path}")

        for i in range(self.valid_test_len):
            file_full_path = os.path.join(self.rejected_path, rejected_list[i])
            shutil.move(file_full_path, self.valid_rejected_path)
        print(f"{self.valid_test_len} images moved to {self.valid_rejected_path}")

    def __test_split(self):
        accepted_list = os.listdir(self.accepted_path)
        rejected_list = os.listdir(self.rejected_path)

        for i in range(self.valid_test_len):
            file_full_path = os.path.join(self.accepted_path, accepted_list[i])
            shutil.move(file_full_path, self.test_path)

        for i in range(self.valid_test_len):
            file_full_path = os.path.join(self.rejected_path, rejected_list[i])
            shutil.move(file_full_path, self.test_path)
        print(f"{self.valid_test_len * 2} images moved to {self.test_path}")

    def __train_split(self):
        accepted_list = os.listdir(self.accepted_path)
        rejected_list = os.listdir(self.rejected_path)

        for i in range(self.train_len):
            file_full_path = os.path.join(self.accepted_path, accepted_list[i])
            shutil.move(file_full_path, self.train_accepted_path)

        for rejected in rejected_list:
            file_full_path = os.path.join(self.rejected_path, rejected)
            shutil.move(file_full_path, self.train_rejected_path)

    def train_test_split(self):
        print("*" * 10, "splitting images", "*" * 10)
        self.__valid_split()
        self.__test_split()
        self.__train_split()


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.realpath(__file__))
    input_dir = os.path.join(current_path, "..", "..", "..", "dataset", "avatars", "tmp2")
    splitter = Splitter(input_dir, False)
    splitter.train_test_split()
