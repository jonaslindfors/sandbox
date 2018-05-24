# Usage

### Import this as a shotgun toolkit app.

1. Download the latest release of this as a .zip.
2. Upload to shotgun as a toolkit app
3. Add the app to your config.

A couple of lines are needed in the before_app_launch.py hook in order to set environment variables for OCIO profile and project colorspace


# FLOW (How the app works.)


### Steps in the app
1. Determines based on template file in config where the luts should be located
2. Downloads correct project lut from shotgun
3. Sets up environment variables for project lut that the OCIO config needs
4. Downloads correct shot lut from shotgun
5. Sets up environment variables for shot lut that the OCIO config needs
6. Sets up OCIO for engine, at the moment only Nuke is supported
#####    tk-nuke
1. Sets color management to OCIO in root tab
2. Loops through all viewers and updates the context tab in the OCIODisplay node with values that the OCIO config will read
3. Adds a onCreate callback to make sure that any new viewers will add the same values to the context tab in the OCIODisplay node


# OCIO workflow in short

We basically have three different lut modes that we need to keep track on:
PROJECT_LUT
SHOT_LUT
SHOT_AND_PROJECT_LUT

Breakdown and examples:

OCIO config for PROJECT_LUT
```yaml
- !<FileTransform> {src: '${PROJECT_COLOR_SPACE}.spi1d', interpolation: linear}
- !<FileTransform> {src: '${PROJECT_LUT_PROCESS_SPACE}.spi1d', interpolation: linear, direction: inverse}
- !<FileTransform> {src: '${PROJECT_LUT}', interpolation: linear}
```

Example 1:
We have a linearized alexa plate that needs to have the alexa to rec709 lut applied
1. Apply lut for project colorspace - Plate is linear and project colorspace is linear, therefore nothing would happen here
2. Apply inverse of process space for project lut - Since the alexa lut has AlexaLogC colorspace as process space, we apply a linear to AlexaLogC transform
3. Apply project lut - Now the plate is prepped and ready to have the alexa to rec709 lut applied

Example 2:
We have a plate in AlexaLogC colorspace that needs to have the alexa to rec709 lut applied
1. Apply lut for project colorspace - Plate is AlexaLogC and project colorspace is AlexaLogC, so here we linearize the plate
2. Apply inverse of process space for project lut - Since the alexa lut has AlexaLogC colorspace as process space, we apply a linear to AlexaLogC transform, so basically we go back to where we were in the first place, but this is needed in order to preserve flexibility for differenet colorspaces 
3. Apply project lut - Now the plate is prepped and ready to have the alexa to rec709 lut applied

The SHOT_LUT works in the same way as the PROJECT_LUT but applies the SHOT_LUT instead of the PROJECT_LUT

OCIO config for SHOT_AND_PROJECT_LUT:
```yaml
- !<FileTransform> {src: '${PROJECT_COLOR_SPACE}.spi1d', interpolation: linear}
- !<FileTransform> {src: '${SHOT_LUT_PROCESS_SPACE}.spi1d', interpolation: linear, direction: inverse}
- !<FileTransform> {src: '${SHOT_LUT}', interpolation: linear} 
- !<FileTransform> {src: '${PROJECT_COLOR_SPACE}.spi1d', interpolation: linear}
- !<FileTransform> {src: '${PROJECT_LUT}', interpolation: linear} 
```

Example 1:
We have a linearized alexa plate that needs to have a shot lut applied and the alexa to rec709 lut on top of that
1. Apply lut for project colorspace - Plate is linear and project colorspace is linear, therefore nothing would happen here
2. Apply inverse of process space for project lut - Since the alexa lut has AlexaLogC colorspace as process space, we apply a linear to AlexaLogC transform
3. Apply shot lut
3. Apply project lut
