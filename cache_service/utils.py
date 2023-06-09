def convert_dict_to_key(params: dict):
    params_keys = params.keys()
    cache_key = "CACHE_KEY_"
    for key in params_keys:
        cache_key = f"{cache_key + key + ':' + str(params.get(key))+'_'}"
    return cache_key

