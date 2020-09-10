import matplotlib.pyplot as plt

"""
A class responsible for plotting the following results:
    - size
    - ssim
    - psnr
"""


class Plotter:
    video_labels = []   # video labels

    def __init__(self, labels: list):
        self.video_labels = labels

    def plot_sizes(self, video_data: list):
        plt.xticks(range(len(video_data) - 1), self.video_labels[1:])
        plt.xlabel('video formatai')
        plt.ylabel('KiB')
        plt.title('video formatų dydžio palyginimas')
        plt.xticks(rotation=90)
        plt.bar(range(len(video_data) - 1), video_data[1:], color='royalblue', alpha=0.9)
        plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y')
        plt.show()

    def plot_ssim(self, video_data: list):
        plt.plot(self.video_labels[1:], video_data[1:], color='red', marker='o')
        plt.xticks(rotation=90)
        plt.xlabel('video formatai', fontsize=14)
        plt.ylabel('ssim', fontsize=14)
        plt.title('video formatų struktūriniai palyginimai', fontsize=14)
        plt.grid(True)
        plt.show()

    def plot_psnr(self, video_data: list):
        plt.plot(self.video_labels[1:], video_data[1:], color='red', marker='o')
        plt.xticks(rotation=90)
        plt.xlabel('video formatai', fontsize=14)
        plt.ylabel('psnr (dB)', fontsize=14)
        plt.title('didžiausias signalo ir triukšmo santykis', fontsize=14)
        plt.grid(True)
        plt.show()
