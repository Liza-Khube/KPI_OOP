import os
import re

class ProjectAnalyzer:
    def __init__(self):
        self.files_data = {}
        self.levels = {}
        self.project_root = ""

    def scan_directory(self, path):

        self.files_data = {}
        
        if os.path.isfile(path):
            self.project_root = os.path.dirname(path)
        else:
            self.project_root = path

        if not self.project_root:
            return

        try:
            all_files = os.listdir(self.project_root)
            code_files = [f for f in all_files if f.endswith(('.cpp', '.h', '.rc'))]
        except OSError as e:
            print(f"Error reading directory: {e}")
            return

        for filename in code_files:
            full_path = os.path.join(self.project_root, filename)
            includes = self._parse_includes(full_path)
            self.files_data[filename] = includes

        self._calculate_levels()

    def _parse_includes(self, file_path):
        includes = []
        regex = re.compile(r'^\s*#include\s+["<](.*?)[">]')
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    match = regex.match(line)
                    if match:
                        included_file = match.group(1)
                        includes.append(os.path.basename(included_file))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
        return includes

    def _calculate_levels(self):
        memo = {}
        visiting = set()
        local_files = set(self.files_data.keys())

        def get_level_dfs(file_node):
            if file_node in memo:
                return memo[file_node]

            if file_node in visiting:
                return -1
            
            visiting.add(file_node)
            
            max_child_level = -1

            dependencies = self.files_data.get(file_node, [])
            
            for dep in dependencies:

                if dep in local_files:
                    child_lvl = get_level_dfs(dep)
                    if child_lvl > max_child_level:
                        max_child_level = child_lvl
            
            my_level = max_child_level + 1
            
            memo[file_node] = my_level
            visiting.remove(file_node)
            
            return my_level

        for file in local_files:
            get_level_dfs(file)
            
        if not memo:
            self.levels = {}
            return

        max_height = max(memo.values())
        
        self.levels = {}
        for file, height in memo.items():
            visual_level = max_height - height
            
            if visual_level not in self.levels:
                self.levels[visual_level] = []
            self.levels[visual_level].append(file)

    def get_hierarchy_data(self):
        return self.levels, self.files_data