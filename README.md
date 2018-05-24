PROJECT_LUT
```yaml
- !<FileTransform> {src: '${PROJECT_COLOR_SPACE}.spi1d', interpolation: linear}
- !<FileTransform> {src: '${PROJECT_LUT_PROCESS_SPACE}.spi1d', interpolation: linear, direction: inverse}
- !<FileTransform> {src: '${PROJECT_LUT}', interpolation: linear}
```
