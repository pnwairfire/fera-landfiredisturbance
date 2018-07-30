#
# Load this script in RStudio to compare disturbance timestep trends by fuelbed and column
# (Landfire was run with updated dbh calculation)
#
# Copy the following folders to the same directory as this script:
# baselineTest1
# deliverablesTest1
#
# set the working directory to the source file location
# From RStudio menu: Session->Set Working Directory->To Source File Location
#
# To run: click the "Source" button (you should see two empty graphs)
# click the gear icon in the top left of the graph to select fuelbed, disturbance, and column
#

library(ggplot2) 
library(manipulate)
library(gridExtra)

fccsBaselineData284 = read.csv("baselineTest1/fccs_summary.csv", header=T)
dim(fccsBaselineData284)

fccsData284 = read.csv("deliverablesTest1/fccs_summary.csv", header=T)
dim(fccsData284)


#add summary columns
#1)     Total Shrub Loading (primary + secondary layer loading)
#2)     Total Herb Loading (primary + secondary layer loading)
#3)     Total CWD loading (sum of all 1000hr, 10,000hr and >10,000hr loads)
#4)     Total FWD loading (sum of 1hr, 10hr and 100hr loads)
#5)     Total Sound Wood loading (sum of all sound wood 1hr to >10,000hr loads)
#6)     Total Rotten Wood loading (sum of rotten wood 1000hr, 10,000hr and >10000hr loads)

fccsBaselineData284[is.na(fccsBaselineData284)] <- 0
fccsBaselineData284$TotalShrubLoading <- fccsBaselineData284$Shrub_primary_load + fccsBaselineData284$Shrub_secondary_load
fccsBaselineData284$TotalHerbLoading <- fccsBaselineData284$Herb_primary_load + fccsBaselineData284$Herb_secondary_load
fccsBaselineData284$TotalCWD <- fccsBaselineData284$Woody_sound_1000hr_load + fccsBaselineData284$Woody_sound_10khr_load + fccsBaselineData284$Woody_sound_GT10k_load
fccsBaselineData284$TotalFWD <- fccsBaselineData284$Woody_sound_1hr_load + fccsBaselineData284$Woody_sound_10hr_load + fccsBaselineData284$Woody_sound_100hr_load
fccsBaselineData284$TotalSoundWoodLoading <- fccsBaselineData284$TotalCWD + fccsBaselineData284$TotalFWD
fccsBaselineData284$TotalRottenWoodLoading <- fccsBaselineData284$Woody_rotten_1000hr_load + fccsBaselineData284$Woody_rotten_10k_load + fccsBaselineData284$Woody_rotten_GT10k_load


fccsData284$TotalShrubLoading <- fccsData284$Shrub_primary_load + fccsData284$Shrub_secondary_load
fccsData284$TotalHerbLoading <- fccsData284$Herb_primary_load + fccsData284$Herb_secondary_load
fccsData284$TotalCWD <- fccsData284$Woody_sound_1000hr_load + fccsData284$Woody_sound_10khr_load + fccsData284$Woody_sound_GT10k_load
fccsData284$TotalFWD <- fccsData284$Woody_sound_1hr_load + fccsData284$Woody_sound_10hr_load + fccsData284$Woody_sound_100hr_load
fccsData284$TotalSoundWoodLoading <- fccsData284$TotalCWD + fccsData284$TotalFWD
fccsData284$TotalRottenWoodLoading <- fccsData284$Woody_rotten_1000hr_load + fccsData284$Woody_rotten_10k_load + fccsData284$Woody_rotten_GT10k_load


myPlot <- function(fb_number, disturbance, columnName){
  
  disturbance <- substring(disturbance, 1, 1)
  
  baselineData284 <- fccsBaselineData284[fccsBaselineData284$Fuelbed_number == fb_number, c('Fuelbed_number', columnName, 'Fuelbed_name')]
  
  bdtest <- paste(fb_number, disturbance, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  fb_data284 <- fccsData284[fccsData284$Fuelbed_number %in% bdtest, c('Fuelbed_number', columnName, 'Fuelbed_name')]
  prefix284 <- substr(fb_data284$Fuelbed_number, 0, nchar(fb_number) + 3)
  timeStep284 <- substr(fb_data284$Fuelbed_number, nchar(fb_number) + 4, nchar(fb_number) + 4)

  fb_data284$Prefix <- prefix284
  fb_data284$TimeStep <- as.numeric(timeStep284)
  
  baselineDataExpanded284 <- baselineData284[rep(row.names(baselineData284), length(unique(fb_data284$Prefix))), 1:3]
  baselineDataExpanded284$Prefix <- unique(fb_data284$Prefix)
  baselineDataExpanded284$TimeStep <- rep(0, length(unique(fb_data284$Prefix)))
  
  combinedData284 <- rbind(fb_data284, baselineDataExpanded284)
  

  mygraph284 <- ggplot(data = combinedData284, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph284 <- mygraph284 + guides(colour=guide_legend(title="Disturbance"))
  mygraph284 <- mygraph284 + ggtitle(paste(combinedData284$Fuelbed_name[1], "Updated dbh Landfire (FCCS build 284)", sep=" ")) + xlim(0,3)
  mygraph284 <- mygraph284 + scale_color_manual(values = c("green4", "orange", "red"))
  
#  grid.arrange(mygraph276, mygraph284, nrow=2)
  mygraph284
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(fccsBaselineData284$Fuelbed_number, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(fccsBaselineData284), as.character)))

