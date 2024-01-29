"""
    This module is used to generate tables and graphs for brochures
"""
import random
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
# -*- coding: utf-8 -*-
cycol = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
words = [
    "привіт",
    "кава",
    "книга",
    "сонце",
    "мова",
    "день",
    "ночі",
    "річка",
    "дерево",
    "пташка"
]


def generate_plot(width, height):
    """
        This function is used to decide on what random plot
        to generate
    """
    choice = random.randint(1, 4)
    dpi = 100
    figsize = (width / dpi, height / dpi)
    f_size = 7

    if choice == 1:
        generate_line_plot(dpi, figsize, f_size)

    elif choice == 2:
        generate_scatter_plot(dpi, figsize, f_size)

    elif choice == 3:
        f_size = 4
        generate_bar_plot(dpi, figsize, f_size)

    elif choice == 4:
        generate_histogram(dpi, figsize, f_size)

    return 'temporary_image.jpg'


def draw_labels(plot, f_size):
    """
        This function is used to draw lables on the plot
    """
    plot.xlabel(random.choice(words), fontsize=f_size)
    plot.ylabel(random.choice(words), fontsize=f_size)
    plot.xticks(fontsize=f_size)
    plot.yticks(fontsize=f_size)


def generate_line_plot(dpi, figsize, f_size):
    """
        This function is used to generate line plot
    """
    num_of_values = random.randint(3, 50)
    x = np.linspace(0, 10, num_of_values)
    y = np.random.uniform(0, 10, num_of_values)
    plt.figure(figsize=figsize, dpi=dpi)
    plt.plot(x, y, color=next(cycol))
    draw_labels(plt, f_size)
    plt.savefig('temporary_image.jpg', bbox_inches='tight', pad_inches=0)


def generate_scatter_plot(dpi, figsize, f_size):
    """
        This function is used to generate scatter plot
    """
    x = np.random.rand(50)
    y = np.random.rand(50)
    plt.figure(figsize=figsize, dpi=dpi)
    plt.scatter(x, y, color=next(cycol))
    draw_labels(plt, f_size)
    plt.savefig('temporary_image.jpg', bbox_inches='tight', pad_inches=0)


def generate_bar_plot(dpi, figsize, f_size):
    """
        This function is used to generate bar plot
    """
    bars = random.randint(3, 6)
    categories = []
    while len(categories) < bars:
        new_category = random.choice(words) + str(random.randint(1, 99))
        if new_category not in categories:
            categories.append(new_category)

    values = [random.randint(5, 50) for _ in range(bars)]
    colors = [next(cycol) for _ in range(bars)]

    plt.figure(figsize=figsize, dpi=dpi)
    plt.bar(categories, values, color=colors)
    draw_labels(plt, f_size)
    plt.savefig('temporary_image.jpg', bbox_inches='tight', pad_inches=0)


def generate_histogram(dpi, figsize, f_size):
    """
        This function is used to generate histogram
    """
    data = np.random.randn(1000)
    plt.figure(figsize=figsize, dpi=dpi)
    plt.hist(data, bins=20, color=next(cycol), edgecolor='black', alpha=0.7)
    draw_labels(plt, f_size)
    plt.savefig('temporary_image.jpg', bbox_inches='tight', pad_inches=0)
