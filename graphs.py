"""
    This module is used to generate tables and graphs for brochures
"""

import random
import itertools
import matplotlib.pyplot as plt
import numpy as np
import text_functions as tf
import constants as c
# -*- coding: utf-8 -*-

cycle_colors = itertools.cycle(plt.cm.tab10.colors)
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


def decide_on_background_coloring_type(brochure, block):
    """
        This function is used to randomly decide on coloring type
        for the graph background
    """

    coloring = np.random.choice(np.arange(1, 4), p=[0.6, 0.2, 0.2])

    if coloring == 1:

        background_color = (1, 1, 1)

    elif coloring == 2:

        cropped = brochure.image.crop((block.x, block.y, block.x + block.width,
                                       block.y + block.height))
        average_color_row = np.average(cropped, axis=0)
        background_color = np.average(average_color_row, axis=0)
        background_color = tuple(value/255 for value in background_color)

    elif coloring == 3:

        background_color = tf.get_random_color(0, 255)
        background_color = tuple(value / 255 for value in background_color)

    return background_color


def generate_plot(brochure, block):
    """
        This function is used to decide on what random plot
        to generate
    """

    background_color = decide_on_background_coloring_type(brochure, block)
    set_background_color(background_color)
    data_color = get_contrasting_color_for_graphs(background_color)

    choice = random.randint(1, 4)
    dpi = 100
    fig_size = (block.width / dpi, block.height / dpi)
    f_size = 7

    if choice == 1:
        generate_line_plot(dpi, fig_size, f_size, background_color, data_color)

    elif choice == 2:
        generate_scatter_plot(dpi, fig_size, f_size, background_color, data_color)

    elif choice == 3:
        f_size = 4
        generate_bar_plot(dpi, fig_size, f_size, background_color)

    elif choice == 4:
        generate_histogram(dpi, fig_size, f_size, background_color, data_color)


def set_background_color(background_color):
    """
        This function is used to set background color for the graph
    """

    plt.rcdefaults()
    plt.rcParams.update({'axes.facecolor': background_color})


def get_contrasting_color_for_graphs(color):
    """
        This function is used to generate contrasting color
        to represent data on the graph
    """

    if random.choice([True, False]):
        color = tuple(int(value * 255) for value in color)
        contrasting_color = tf.get_contrasting_color(color=color)
        contrasting_color = tuple(value / 255 for value in contrasting_color)
        return contrasting_color

    return next(cycle_colors)


def decide_on_grid():
    """
        This function is used to randomly decide whether to use grid
        on the graph
    """

    if random.choice([True, False]):
        plt.grid()


def draw_labels(plot, f_size):
    """
        This function is used to draw labels on the plot
    """

    plot.xlabel(random.choice(words), fontsize=f_size)
    plot.ylabel(random.choice(words), fontsize=f_size)
    plot.xticks(fontsize=f_size)
    plot.yticks(fontsize=f_size)


def generate_line_plot(dpi, fig_size, f_size, background_color, data_color):
    """
        This function is used to generate line plot
    """

    num_of_values = random.randint(3, 25)
    x = np.linspace(0, 10, num_of_values)
    y = np.random.uniform(0, 10, num_of_values)
    plt.figure(figsize=fig_size, dpi=dpi, facecolor=background_color)
    plt.plot(x, y, color=data_color)
    draw_labels(plt, f_size)
    decide_on_grid()
    plt.savefig(c.TEMPORARY_IMAGE, bbox_inches='tight', pad_inches=0)


def generate_scatter_plot(dpi, fig_size, f_size, background_color, data_color):
    """
        This function is used to generate scatter plot
    """

    x = np.random.rand(50)
    y = np.random.rand(50)
    plt.figure(figsize=fig_size, dpi=dpi, facecolor=background_color)
    plt.scatter(x, y, color=data_color)
    draw_labels(plt, f_size)
    decide_on_grid()
    plt.savefig(c.TEMPORARY_IMAGE, bbox_inches='tight', pad_inches=0)


def generate_bar_plot(dpi, fig_size, f_size, background_color):
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
    colors = [get_contrasting_color_for_graphs(background_color) for _ in range(bars)]

    plt.figure(figsize=fig_size, dpi=dpi, facecolor=background_color)
    plt.bar(categories, values, color=colors)
    draw_labels(plt, f_size)
    decide_on_grid()
    plt.savefig(c.TEMPORARY_IMAGE, bbox_inches='tight', pad_inches=0)


def generate_histogram(dpi, fig_size, f_size, background_color, data_color):
    """
        This function is used to generate histogram
    """

    data = np.random.randn(1000)
    plt.figure(figsize=fig_size, dpi=dpi, facecolor=background_color)
    plt.hist(data, bins=20, color=data_color, edgecolor='black', alpha=0.7)
    draw_labels(plt, f_size)
    decide_on_grid()
    plt.savefig(c.TEMPORARY_IMAGE, bbox_inches='tight', pad_inches=0)
