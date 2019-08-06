#!/usr/bin/env python
#encoding=utf-8

from flask import Flask, render_template, request, url_for
import json

def map_data():
    route_dict = {'0-0': [], '0-1': [[0, 5], [5, 16], [16, 1]], '0-2': [], '0-3': [], '0-4': [], 
        '0-5': [[0, 5]], '0-6': [], '0-7': [[0, 7]], '0-8': [], '0-9': [], '0-10': [], 
        '0-11': [], '0-12': [], '0-13': [[0, 7], [7, 9], [9, 13]], '0-14': [], 
        '0-15': [[0, 15]], '0-16': [], '0-17': [], '0-18': [], '0-19': [], 
        '0-20': [[0, 5], [0, 5], [0, 7], [0, 7], [0, 15], [5, 16], [7, 9], [9, 13], [16, 1]], 
        '1-0': [], '1-1': [], '1-2': [], '1-3': [], '1-4': [], '1-5': [[1, 8], [8, 5]],
        '1-6': [], '1-7': [], '1-8': [], '1-9': [], '1-10': [], '1-11': [], '1-12': [], 
        '1-13': [], '1-14': [], '1-15': [[1, 15]], '1-16': [], '1-17': [], '1-18': [], 
        '1-19': [], '1-20': [[1, 8], [1, 15], [8, 5]], '2-0': [], '2-1': [[2, 6], [6, 1]], 
        '2-2': [], '2-3': [], '2-4': [], '2-5': [], '2-6': [], '2-7': [], '2-8': [], 
        '2-9': [[2, 6], [6, 15], [15, 9]], '2-10': [], '2-11': [], '2-12': [], '2-13': [], 
        '2-14': [], '2-15': [], '2-16': [], '2-17': [[1, 17], [2, 1]], 
        '2-18': [[1, 18], [2, 1]], '2-19': [], '2-20': [[1, 17], [1, 18], [2, 1], [2, 1], [2, 6], [2, 6], [6, 1], [6, 15], [15, 9]], '3-0': [], '3-1': [], 
        '3-2': [[3, 15], [15, 2]], '3-3': [], '3-4': [[3, 15], [15, 4]], '3-5': [], '3-6': [[3, 6]], 
        '3-7': [], '3-8': [], '3-9': [], '3-10': [], '3-11': [], '3-12': [], '3-13': [], 
        '3-14': [], '3-15': [], '3-16': [[1, 16], [3, 15], [15, 1]], '3-17': [], '3-18': [], 
        '3-19': [[3, 7], [7, 9], [9, 19]], '3-20': [[1, 16], [3, 6], [3, 7], [3, 15], [3, 15], [3, 15], [7, 9], [9, 19], [15, 1], [15, 2], [15, 4]], '4-0': [], '4-1': [], 
        '4-2': [[4, 14], [14, 15], [15, 2]], '4-3': [], '4-4': [], '4-5': [[1, 5], [4, 14], [14, 1]], 
        '4-6': [], '4-7': [], '4-8': [], '4-9': [], '4-10': [[1, 10], [4, 14], [14, 1]], 
        '4-11': [], '4-12': [], '4-13': [], '4-14': [[4, 14]], '4-15': [], '4-16': [], 
        '4-17': [], '4-18': [], '4-19': [], '4-20': [[1, 5], [1, 10], [4, 14], [4, 14], [4, 14], [4, 14], [14, 1], [14, 1], [14, 15], [15, 2]], '5-0': [], '5-1': [], 
        '5-2': [], '5-3': [], '5-4': [], '5-5': [], '5-6': [], '5-7': [[5, 12], [12, 7]], 
        '5-8': [], '5-9': [], '5-10': [], '5-11': [], '5-12': [], '5-13': [[5, 12], [12, 13]], 
        '5-14': [], '5-15': [], '5-16': [[5, 16]], '5-17': [], '5-18': [[1, 18], [5, 16], [16, 1]], 
        '5-19': [], '5-20': [[1, 18], [5, 12], [5, 12], [5, 16], [5, 16], [12, 7], [12, 13], [16, 1]], 
        '6-0': [[1, 0], [6, 1]], '6-1': [], '6-2': [], '6-3': [], '6-4': [], '6-5': [[1, 5], [6, 1]], 
        '6-6': [], '6-7': [], '6-8': [], '6-9': [[6, 15], [15, 9]], '6-10': [[1, 10], [6, 1]], 
        '6-11': [[6, 15], [15, 11]], '6-12': [[6, 15], [15, 12]], '6-13': [], '6-14': [], 
        '6-15': [[6, 15]], '6-16': [], '6-17': [[1, 17], [6, 1]], '6-18': [], '6-19': [], 
        '6-20': [[1, 0], [1, 5], [1, 10], [1, 17], [6, 1], [6, 1], [6, 1], [6, 1], [6, 15], [6, 15], [6, 15], [6, 15], [15, 9], [15, 11], [15, 12]], '7-0': [], '7-1': [], 
        '7-2': [], '7-3': [], '7-4': [], '7-5': [], '7-6': [], '7-7': [], '7-8': [], 
        '7-9': [], '7-10': [], '7-11': [], '7-12': [], '7-13': [], '7-14': [[4, 14], [7, 4]], '7-15': [], '7-16': [], '7-17': [], '7-18': [], '7-19': [[7, 9], [9, 19]], 
        '7-20': [[4, 14], [7, 4], [7, 9], [9, 19]], '8-0': [], '8-1': [], '8-2': [[1, 15], [8, 1], [15, 2]], 
        '8-3': [[1, 15], [8, 1], [15, 3]], '8-4': [], '8-5': [], '8-6': [], '8-7': [], 
        '8-8': [], '8-9': [[1, 9], [8, 14], [14, 1]], '8-10': [], '8-11': [], '8-12': [[5, 12], [8, 5]], 
        '8-13': [], '8-14': [], '8-15': [[1, 15], [8, 1]], '8-16': [[5, 16], [8, 5]], 
        '8-17': [], '8-18': [], '8-19': [], '8-20': [[1, 9], [1, 15], [1, 15], [1, 15], [5, 12], [5, 16], [8, 1], [8, 1], [8, 1], [8, 5], [8, 5], [8, 14], [14, 1], [15, 2], [15, 3]], 
        '9-0': [], '9-1': [], '9-2': [], '9-3': [[9, 15], [15, 3]], '9-4': [[9, 15], [15, 4]], 
        '9-5': [], '9-6': [], '9-7': [], '9-8': [], '9-9': [], '9-10': [], '9-11': [], 
        '9-12': [], '9-13': [], '9-14': [[4, 14], [9, 15], [15, 4]], '9-15': [], '9-16': [], 
        '9-17': [], '9-18': [], '9-19': [[9, 19]], '9-20': [[4, 14], [9, 15], [9, 15], [9, 15], [9, 19], [15, 3], [15, 4], [15, 4]], '10-0': [[10, 0]], '10-1': [], '10-2': [[10, 15], [15, 2]], 
        '10-3': [], '10-4': [], '10-5': [[1, 5], [10, 1]], '10-6': [[10, 6]], '10-7': [], 
        '10-8': [[1, 8], [10, 1]], '10-9': [], '10-10': [], '10-11': [], '10-12': [], 
        '10-13': [], '10-14': [], '10-15': [], '10-16': [], '10-17': [], '10-18': [], 
        '10-19': [], '10-20': [[1, 5], [1, 8], [10, 0], [10, 1], [10, 1], [10, 6], [10, 15], [15, 2]], '11-0': [[1, 0], [11, 1]], '11-1': [[11, 1]], '11-2': [[11, 2]], 
        '11-3': [], '11-4': [], '11-5': [[1, 5], [11, 1]], '11-6': [[2, 6], [11, 2]], 
        '11-7': [], '11-8': [], '11-9': [], '11-10': [], '11-11': [], '11-12': [], 
        '11-13': [], '11-14': [], '11-15': [], '11-16': [[1, 16], [11, 1]], '11-17': [], 
        '11-18': [[1, 18], [11, 1]], '11-19': [], '11-20': [[1, 0], [1, 5], [1, 16], [1, 18], [2, 6], [11, 1], [11, 1], [11, 1], [11, 1], [11, 1], [11, 2], [11, 2]], 
        '12-0': [[10, 0], [12, 10]], '12-1': [[10, 1], [12, 10]], '12-2': [], '12-3': [], 
        '12-4': [], '12-5': [], '12-6': [], '12-7': [], '12-8': [], '12-9': [[7, 9], [12, 7]], '12-10': [[12, 10]], '12-11': [], '12-12': [], '12-13': [], '12-14': [], 
        '12-15': [], '12-16': [], '12-17': [], '12-18': [], '12-19': [[7, 9], [9, 19], [12, 7]], 
        '12-20': [[7, 9], [7, 9], [9, 19], [10, 0], [10, 1], [12, 7], [12, 7], [12, 10], [12, 10], [12, 10]], 
        '13-0': [], '13-1': [], '13-2': [[1, 15], [13, 1], [15, 2]], '13-3': [], '13-4': [], '13-5': [], '13-6': [[1, 15], [13, 1], [15, 6]], 
        '13-7': [], '13-8': [], '13-9': [], '13-10': [], '13-11': [], '13-12': [], 
        '13-13': [], '13-14': [], '13-15': [[7, 9], [9, 15], [13, 7]], '13-16': [[1, 16], [13, 1]], 
        '13-17': [[1, 17], [13, 1]], '13-18': [[1, 18], [13, 1]], '13-19': [[7, 9], [9, 19], [13, 7]], 
        '13-20': [[1, 15], [1, 15], [1, 16], [1, 17], [1, 18], [7, 9], [7, 9], [9, 15], [9, 19], [13, 1], [13, 1], [13, 1], [13, 1], [13, 1], [13, 7], [13, 7], [15, 2], [15, 6]], 
        '14-0': [], '14-1': [], '14-2': [[14, 15], [15, 2]], '14-3': [], '14-4': [], 
        '14-5': [], '14-6': [[3, 6], [14, 15], [15, 3]], '14-7': [], '14-8': [], '14-9': [], 
        '14-10': [], '14-11': [], '14-12': [], '14-13': [[1, 9], [9, 13], [14, 1]], 
        '14-14': [], '14-15': [], '14-16': [[1, 16], [14, 1]], '14-17': [], '14-18': [[1, 18], [14, 1]], 
        '14-19': [], '14-20': [[1, 9], [1, 16], [1, 18], [3, 6], [9, 13], [14, 1], [14, 1], [14, 1], [14, 15], [14, 15], [15, 2], [15, 3]], '15-0': [], 
        '15-1': [], '15-2': [], '15-3': [], '15-4': [], '15-5': [], '15-6': [[15, 6]], 
        '15-7': [], '15-8': [], '15-9': [], '15-10': [], '15-11': [], '15-12': [[15, 12]], 
        '15-13': [], '15-14': [[4, 14], [15, 4]], '15-15': [], '15-16': [], '15-17': [], 
        '15-18': [[1, 18], [15, 1]], '15-19': [[9, 19], [15, 9]], '15-20': [[1, 18], [4, 14], [9, 19], [15, 1], [15, 4], [15, 6], [15, 9], [15, 12]], 
        '16-0': [[1, 0], [16, 1]], '16-1': [], '16-2': [], '16-3': [[1, 15], [15, 3], [16, 1]], '16-4': [], 
        '16-5': [], '16-6': [], '16-7': [], '16-8': [], '16-9': [], '16-10': [], '16-11': [], 
        '16-12': [], '16-13': [], '16-14': [], '16-15': [], '16-16': [], '16-17': [], 
        '16-18': [], '16-19': [[1, 9], [9, 19], [16, 1]], '16-20': [[1, 0], [1, 9], [1, 15], [9, 19], [15, 3], [16, 1], [16, 1], [16, 1]], '17-0': [[1, 0], [17, 1]], 
        '17-1': [], '17-2': [], '17-3': [], '17-4': [], '17-5': [[1, 5], [17, 1]], '17-6': [[1, 15], [15, 6], [17, 1]], '17-7': [], '17-8': [], '17-9': [], '17-10': [], 
        '17-11': [], '17-12': [[1, 5], [5, 12], [17, 1]], '17-13': [], '17-14': [], 
        '17-15': [], '17-16': [[1, 16], [17, 1]], '17-17': [], '17-18': [[1, 18], [17, 1]], 
        '17-19': [[1, 9], [9, 19], [17, 1]], '17-20': [[1, 0], [1, 5], [1, 5], [1, 9], [1, 15], [1, 16], [1, 18], [5, 12], [9, 19], [15, 6], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1]], 
        '18-0': [[18, 0]], '18-1': [], '18-2': [[15, 2], [18, 15]], '18-3': [], '18-4': [], 
        '18-5': [], '18-6': [], '18-7': [], '18-8': [], '18-9': [[0, 7], [7, 9], [18, 0]], 
        '18-10': [], '18-11': [], '18-12': [], '18-13': [[0, 7], [7, 13], [18, 0]], 
        '18-14': [], '18-15': [], '18-16': [], '18-17': [], '18-18': [], '18-19': [], 
        '18-20': [[0, 7], [0, 7], [7, 9], [7, 13], [15, 2], [18, 0], [18, 0], [18, 0], [18, 15]], 
        '19-0': [[10, 0], [19, 10]], '19-1': [[10, 1], [19, 10]], '19-2': [[10, 15], [15, 2], [19, 10]], '19-3': [[10, 15], [15, 3], [19, 10]], '19-4': [], '19-5': [], 
        '19-6': [], '19-7': [], '19-8': [], '19-9': [[7, 9], [13, 7], [19, 13]], '19-10': [], '19-11': [], '19-12': [], '19-13': [[19, 13]], '19-14': [], '19-15': [], 
        '19-16': [], '19-17': [[1, 17], [13, 1], [19, 13]], '19-18': [], '19-19': [], 
        '19-20': [[1, 17], [7, 9], [10, 0], [10, 1], [10, 15], [10, 15], [13, 1], [13, 7], [15, 2], [15, 3], [19, 10], [19, 10], [19, 10], [19, 10], [19, 13], [19, 13], [19, 13]], 
        '20-0': [[1, 0], [1, 0], [1, 0], [1, 0], [6, 1], [10, 0], [10, 0], [10, 0], [11, 1], [12, 10], [16, 1], [17, 1], [18, 0], [19, 10]], 
        '20-1': [[0, 5], [2, 6], [5, 16], [6, 1], [10, 1], [10, 1], [11, 1], [12, 10], [16, 1], [19, 10]], 
        '20-2': [[1, 15], [1, 15], [3, 15], [4, 14], [8, 1], [10, 15], [10, 15], [11, 2], [13, 1], [14, 15], [14, 15], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [18, 15], [19, 10]], 
        '20-3': [[1, 15], [1, 15], [8, 1], [9, 15], [10, 15], [15, 3], [15, 3], [15, 3], [15, 3], [16, 1], [19, 10]], 
        '20-4': [[3, 15], [9, 15], [15, 4], [15, 4]], '20-5': [[0, 5], [1, 5], [1, 5], [1, 5], [1, 5], [1, 5], [1, 8], [4, 14], [6, 1], [8, 5], [10, 1], [11, 1], [14, 1], [17, 1]], 
        '20-6': [[1, 15], [1, 15], [2, 6], [3, 6], [3, 6], [10, 6], [11, 2], [13, 1], [14, 15], [15, 3], [15, 6], [15, 6], [15, 6], [17, 1]], '20-7': [[0, 7], [5, 12], [12, 7]], 
        '20-8': [[1, 8], [10, 1]], 
        '20-9': [[0, 7], [1, 9], [2, 6], [6, 15], [6, 15], [7, 9], [7, 9], [7, 9], [8, 14], [12, 7], [13, 7], [14, 1], [15, 9], [15, 9], [18, 0], [19, 13]], 
        '20-10': [[1, 10], [1, 10], [4, 14], [6, 1], [12, 10], [14, 1]], 
        '20-11': [[6, 15], [15, 11]], '20-12': [[1, 5], [5, 12], [5, 12], [6, 15], [8, 5], [15, 12], [15, 12], [17, 1]], 
        '20-13': [[0, 7], [0, 7], [1, 9], [5, 12], [7, 9], [7, 13], [9, 13], [9, 13], [12, 13], [14, 1], [18, 0], [19, 13]], 
        '20-14': [[4, 14], [4, 14], [4, 14], [4, 14], [7, 4], [9, 15], [15, 4], [15, 4]], 
        '20-15': [[0, 15], [1, 15], [1, 15], [6, 15], [7, 9], [8, 1], [9, 15], [13, 7]], 
        '20-16': [[1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [3, 15], [5, 16], [5, 16], [8, 5], [11, 1], [13, 1], [14, 1], [15, 1], [17, 1]], 
        '20-17': [[1, 17], [1, 17], [1, 17], [1, 17], [2, 1], [6, 1], [13, 1], [13, 1], [19, 13]], 
        '20-18': [[1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [2, 1], [5, 16], [11, 1], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1]], 
        '20-19': [[1, 9], [1, 9], [3, 7], [7, 9], [7, 9], [7, 9], [7, 9], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [12, 7], [13, 7], [15, 9], [16, 1], [17, 1]], 
        '20-20': [[0, 5], [0, 5], [0, 7], [0, 7], [0, 7], [0, 7], [0, 15], [1, 0], [1, 0], [1, 0], [1, 0], [1, 5], [1, 5], [1, 5], [1, 5], [1, 5], [1, 5], [1, 8], [1, 8], [1, 9], [1, 9], [1, 9], [1, 9], [1, 10], [1, 10], [1, 15], [1, 15], [1, 15], [1, 15], [1, 15], [1, 15], [1, 15], [1, 15], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 17], [1, 17], [1, 17], [1, 17], [1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [1, 18], [2, 1], [2, 1], [2, 6], [2, 6], [2, 6], [3, 6], [3, 6], [3, 7], [3, 15], [3, 15], [3, 15], [4, 14], [4, 14], [4, 14], [4, 14], [4, 14], [4, 14], [4, 14], [5, 12], [5, 12], [5, 12], [5, 12], [5, 16], [5, 16], [5, 16], [5, 16], [6, 1], [6, 1], [6, 1], [6, 1], [6, 1], [6, 15], [6, 15], [6, 15], [6, 15], [6, 15], [7, 4], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 13], [8, 1], [8, 1], [8, 1], [8, 5], [8, 5], [8, 5], [8, 14], [9, 13], [9, 13], [9, 15], [9, 15], [9, 15], [9, 15], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [9, 19], [10, 0], [10, 0], [10, 0], [10, 1], [10, 1], [10, 1], [10, 1], [10, 6], [10, 15], [10, 15], [10, 15], [11, 1], [11, 1], [11, 1], [11, 1], [11, 1], [11, 2], [11, 2], [12, 7], [12, 7], [12, 7], [12, 10], [12, 10], [12, 10], [12, 13], [13, 1], [13, 1], [13, 1], [13, 1], [13, 1], [13, 1], [13, 7], [13, 7], [13, 7], [14, 1], [14, 1], [14, 1], [14, 1], [14, 1], [14, 1], [14, 15], [14, 15], [14, 15], [15, 1], [15, 1], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 2], [15, 3], [15, 3], [15, 3], [15, 3], [15, 3], [15, 4], [15, 4], [15, 4], [15, 4], [15, 6], [15, 6], [15, 6], [15, 9], [15, 9], [15, 9], [15, 11], [15, 12], [15, 12], [16, 1], [16, 1], [16, 1], [16, 1], [16, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [17, 1], [18, 0], [18, 0], [18, 0], [18, 15], [19, 10], [19, 10], [19, 10], [19, 10], [19, 13], [19, 13], [19, 13]]}
    return route_dict