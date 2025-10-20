import matplotlib
matplotlib.use('Agg')  # Работает без GUI (важно для Jenkins)
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--passed', type=int, default=0)
    parser.add_argument('--failed', type=int, default=0)
    parser.add_argument('--skipped', type=int, default=0)
    parser.add_argument('--duration', type=str, default='00:00')
    parser.add_argument('--test-type', type=str, default='all')
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()

    total = max(1, args.passed + args.failed + args.skipped)

    colors = ['#4CAF50', '#F44336', '#FFC107']
    labels = []
    sizes = []
    actual_colors = []

    if args.passed > 0:
        labels.append('Passed')
        sizes.append(args.passed)
        actual_colors.append(colors[0])
    if args.failed > 0:
        labels.append('Failed')
        sizes.append(args.failed)
        actual_colors.append(colors[1])
    if args.skipped > 0:
        labels.append('Skipped')
        sizes.append(args.skipped)
        actual_colors.append(colors[2])

    if not sizes:
        labels = ['No tests']
        sizes = [1]
        actual_colors = ['#9E9E9E']

    # Создаём donut chart
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, _ = ax.pie(
        sizes,
        colors=actual_colors,
        wedgeprops=dict(width=0.5),
        startangle=90
    )

    # Текст в центре: "5/6 ✅"
    ax.text(0, 0, f'{args.passed}/{total}\n✅', ha='center', va='center', fontsize=18, fontweight='bold')

    # Легенда справа
    ax.legend(wedges, labels, title="Результаты", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Заголовок
    plt.title(f'Тесты: {args.test_type.upper()}\nДлительность: {args.duration}', fontsize=12, pad=20)

    plt.tight_layout()
    plt.savefig(args.output, dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()