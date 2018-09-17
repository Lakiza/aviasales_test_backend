def deepMergeDict(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deepMergeDict(value, node)
        else:
            destination[key] = value

    return destination

def getDictValueByPath(dictionary, path):
    if not isinstance(dictionary, dict):
        return None

    if "." in path:
        key, rest = path.split(".", 1)
        return (
            getDictValueByPath(dictionary[key], rest)
            if key in dictionary.keys()
            else None
        )
    else:
        return (
            dictionary[path] 
            if path in dictionary.keys() 
            else None
        )
        