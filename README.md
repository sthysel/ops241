# OmniPreSense OPS241 Radar driver

A tool to configure the OmniPreSense OPS241 Radar unit.

## ops241-radar usage

```zsh
Usage: ops241 [OPTIONS]

  OPS241 Radar command tool

Options:
  --version               Show the version and exit.
  -p, --port TEXT         TTY Port radar is available at  [default: /dev/ttyACM0]
  -j, --json-format TEXT  JSON Output format  [default: True]
  -m, --metric TEXT       Use metric units  [default: True]
  --help                  Show this message and exit.
```

## Output

```zsh
{"OutputFeature":"J"}
{"OutputFeature":"M"}
{"Product":"OPS241"}
{"Version":"1.3.0"}
{"SamplingRate":5000, "resolution":0.0995}
{"SampleSize":1024}
{"Clock":"88648"}
{"Q2COUNT":"1150 (~23000 counts/sec) @t=88648"}
{"PowerMode":"Continuous"}
{"Squelch":"1000"}
{"RequiredMinSpeed":"0.000"}
{"magnitude":"467.72","speed":"-0.25","distance":"0.00"}
{"magnitude":"362.44","speed":"-0.35","distance":"0.00"}
{"magnitude":"166.39","speed":"-1.44","distance":"0.00"}
{"magnitude":"170.31","speed":"-1.24","distance":"0.00"}
{"magnitude":"165.46","speed":"-1.44","distance":"0.00"}
{"magnitude":"117.24","speed":"-0.45","distance":"0.00"}
{"magnitude":"130.33","speed":"-1.44","distance":"0.00"}
{"magnitude":"78.59","speed":"-0.55","distance":"0.00"}
{"magnitude":"139.40","speed":"-1.05","distance":"0.00"}
{"magnitude":"118.74","speed":"0.45","distance":"0.00"}
{"magnitude":"161.28","speed":"-0.25","distance":"0.00"}
{"magnitude":"108.46","speed":"-0.65","distance":"0.00"}
{"magnitude":"418.98","speed":"-0.85","distance":"0.00"}
```
