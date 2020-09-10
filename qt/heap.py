def refresh():
    from sys import implementation
    
    if implementation.name == 'micropython':
        from gc import collect, threshold, mem_free, mem_alloc
        collect()
        threshold(mem_free() // 4 + mem_alloc())
