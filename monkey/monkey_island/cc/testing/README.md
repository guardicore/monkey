# Profiling island

To profile specific methods on island a `@profile(sort_args=['cumulative'], print_args=[100])` 
decorator can be used. 
Use it as any other decorator. After decorated method is used, a file will appear in a
directory provided in `profiler_decorator.py`. Filename describes the path of
the method that was profiled. For example if method `monkey_island/cc/resources/netmap.get`
was profiled, then the results of this profiling will appear in 
`monkey_island_cc_resources_netmap_get`.
