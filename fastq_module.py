import gzip
import os
import matplotlib.pyplot as plt

class FastqStats:
    def __init__(self):
        self.n_reads = 0
        self.length_counts = {}
        self._q_sums = []
        self._q_counts = []
        self._b_counts = {b: [] for b in "ACGTN"}

    def add(self, seq, qual):
        self.n_reads += 1
        length = len(seq)
        self.length_counts[length] = self.length_counts.get(length, 0) + 1

        if length > len(self._q_sums):
            diff = length - len(self._q_sums)
            self._q_sums.extend([0] * diff)
            self._q_counts.extend([0] * diff)
            for b in self._b_counts:
                self._b_counts[b].extend([0] * diff)

        for i, (s, q) in enumerate(zip(seq.upper(), qual)):
            self._q_sums[i] += ord(q) - 33
            self._q_counts[i] += 1
            if s in self._b_counts:
                self._b_counts[s][i] += 1

    @property
    def mean_quality(self):
        return [qs / max(qc, 1) for qs, qc in zip(self._q_sums, self._q_counts)]

    @property
    def base_content(self):
        # Заменили pandas на простой словарь со списками
        data = {b: [bc / max(qc, 1) * 100 for bc, qc in zip(self._b_counts[b], self._q_counts)] for b in "ACGTN"}
        return data

class FastqReader:
    def __init__(self, filename):
        self.filename = filename
        self._file = None

    def _open(self):
        if str(self.filename).endswith(".gz"):
            return gzip.open(self.filename, "rt")
        return open(self.filename, "r")

    def __enter__(self):
        self._file = self._open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()

    def __iter__(self):
        with self._open() as f:
            record_no = 0
            while True:
                header = f.readline()
                if not header:
                    break
                if not header.strip():
                    continue
                record_no += 1
                seq = f.readline().strip()
                plus = f.readline().strip()
                qual = f.readline().strip()

                if not header.startswith("@"):
                    raise ValueError(f"Запись {record_no}: нет '@' в заголовке")
                if not plus.startswith("+"):
                    raise ValueError(f"Запись {record_no}: нет '+' в 3-й строке")
                if len(seq) != len(qual):
                    raise ValueError(f"Запись {record_no}: длина seq ({len(seq)}) не равна длине qual ({len(qual)})")
                yield header[1:].strip(), seq, qual

    def compute_stats(self):
        stats = FastqStats()
        for _, seq, qual in self:
            stats.add(seq, qual)
        return stats

    def plot_all(self):
        stats = self.compute_stats()
        
        # Чтобы окна не наслаивались друг на друга, мы создадим одно большое окно с 3 графиками
        fig, axs = plt.subplots(3, 1, figsize=(8, 12))
        fig.canvas.manager.set_window_title('FastQC Статистика')

        # 1. Среднее качество
        axs[0].plot(range(1, len(stats.mean_quality) + 1), stats.mean_quality, color="blue")
        axs[0].set_title("Per base sequence quality")
        axs[0].set_xlabel("Позиция")
        axs[0].set_ylabel("Качество (Phred)")

        # 2. Состав нуклеотидов
        content = stats.base_content
        positions = range(1, len(content["A"]) + 1)
        for b in "ACGTN":
            axs[1].plot(positions, content[b], label=b)
        axs[1].set_title("Per base sequence content")
        axs[1].set_xlabel("Позиция")
        axs[1].set_ylabel("Нуклеотид, %")
        axs[1].legend()

        # 3. Распределение длин
        axs[2].bar(stats.length_counts.keys(), stats.length_counts.values(), color="green")
        axs[2].set_title("Sequence length distribution")
        axs[2].set_xlabel("Длина (bp)")
        axs[2].set_ylabel("Количество ридов")

        plt.tight_layout()
        plt.show()
        return stats