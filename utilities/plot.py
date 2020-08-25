import matplotlib.pyplot as plt

"""
A class responsible for plotting the following results:
    - size
    - ssim
"""


class Plotter:
    video_labels = []   # video labels

    def __init__(self, labels: list):
        self.video_labels = labels

    def plot_sizes(self, video_data: list):
        plt.xticks(range(len(video_data)), self.video_labels)
        plt.xlabel('video formatai')
        plt.ylabel('KiB')
        plt.title('video formatų dydžio palyginimas')

        plt.xticks(rotation=90)
        plt.bar(range(len(video_data)), video_data, color='royalblue', alpha=0.9)
        plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y')
        plt.show()
