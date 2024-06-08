import pathlib
import numpy as np
from sklearn.cluster import DBSCAN
import datetime as dt
import os

from core.dto import Data
from core.ReverseGeocoder import ReverseGeocoder


class AutoSave:
    def __init__(self, path:pathlib.Path, paths:list[pathlib.Path], data:Data) -> None:
        self.__path: pathlib.Path = path
        self.__paths: list[pathlib.Path] = paths
        self.__data: Data = data
        
    def organization(self) -> None:
        location_dict = self.__cluster_photos_by_location()
        directory = {"dailiy":[]}
        max_k = max(location_dict.keys(), key = lambda x: len(location_dict[x]) if x != -1 else 0)
        for k in location_dict:
            if k == -1:
                directory["dailiy"].extend(location_dict[-1])
                continue
            elif k == max_k:
                directory["dailiy"].extend(location_dict[k])
                continue
            elif len(directory[k]) == 0: continue
            location = ReverseGeocoder.get_location_name(k[0], k[1])
            name = f"{location['country']}_{location['city']}"
            paths = location_dict[k]
            date_dict = self.__cluster_photos_by_day(paths)
            for dk in date_dict:
                if dk == -1:
                    if name in directory: directory[name].extend(date_dict[dk])
                    else: directory[name] = date_dict[dk]
                    continue
                elif len(date_dict[dk]) == 0: continue
                d_name = f"{name}_{dt.date.fromordinal(dk[0]).strftime('%Y-%m-%d')}~{dt.date.fromordinal(dk[1]).strftime('%Y-%m-%d')}"
                if d_name in directory: directory[d_name].extend(date_dict[dk])
                else: directory[d_name] = date_dict[dk]
        
        for k in directory:
            dir_path = self.__path / k
            os.makedirs(dir_path, exist_ok=True)
            for p in directory[k]:
                dest = dir_path / p.name
                p.rename(dest)
                self.__data.delete(p)
                self.__paths[self.__paths.index(p)] = dest
        
    def __cluster_photos_by_location(self) -> dict[int | tuple[int, int], list[pathlib.Path]]:
        coords = []
        paths = []
        cluster = {-1:[]}
        for p in self.__paths:
            image = self.__data.get_image(p)
            if image.latitude is not None and image.longitude is not None:
                coords.append([image.latitude, image.longitude])
                paths.append(p)
            else :
                cluster[-1].append(p)
                
        if len(paths) == 0:
            return cluster
        
        coords = np.array(coords)

        clustering = DBSCAN(eps=0.01, min_samples=5).fit(coords)
        labels = clustering.labels_
        
        for label in set(labels):
            if label == -1:
                cluster[label] = [path for path, lbl in zip(paths, labels) if lbl == label]
                continue
            cluster_coords = coords[labels == label]
            center = cluster_coords.mean(axis=0)
            cluster[(center[0], center[1])] = [path for path, lbl in zip(paths, labels) if lbl == label]

        return cluster
    
    def __cluster_photos_by_day(self, source:list[pathlib.Path]) -> dict[int, list[pathlib.Path]]:
        dates = []
        paths = []
        cluster = {-1:[]}
        for p in source:
            date = self.__data.get_image(p).date
            if date is not None:
                dates.append(date.toordinal())
                paths.append(p)
            else :
                cluster[-1].append(p)
                
        if len(paths) == 0:
            return cluster
        
        dates = np.array(dates).reshape(-1, 1)

        clustering = DBSCAN(eps=1, min_samples=1).fit(dates)
        labels = clustering.labels_
        
        for label in set(labels):
            if label == -1:
                cluster[label] = [path for path, lbl in zip(paths, labels) if lbl == label]
                continue
            cluster_dates = dates[labels == label]
            min, max = cluster_dates.min(axis=0), cluster_dates.max(axis=0)
            cluster[(min[0], max[0])] = [path for path, lbl in zip(paths, labels) if lbl == label]

        return cluster