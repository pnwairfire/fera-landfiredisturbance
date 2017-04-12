# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Drive the calculations of the entire suite of disturbances against the fuelbeds that ship with FFT
#                   Run FCCS on the generated fuelbeds
#                    - produces FCCS results .csv file
#                    - produces a Consume loadings file
#                    - third file that Susan needs to specify
#
# =============================================================================


# Get the appropriate fuelbeds
# wget http://172.16.0.120:8081/artifactory/generic-local/Fuelbeds/3.0/fuelbeds.zip