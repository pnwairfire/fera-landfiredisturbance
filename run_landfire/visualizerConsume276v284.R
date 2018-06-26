#
# Load this script in RStudio to compare disturbance timestep trends by fuelbed and column
#
# Copy the following folders to the same directory as this script:
# baseline276
# deliverables276
# baseline284
# deliverables284
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

consumeBaselineData284 = read.csv("baseline284/consume_loadings.csv", header=T, skip=1)
dim(consumeBaselineData284)

consumeData284 = read.csv("deliverables284/consume_loadings.csv", header=T, skip=1)
dim(consumeData284)

consumeBaselineData276 = read.csv("baseline276/consume_loadings.csv", header=T, skip=1)
dim(consumeBaselineData276)

consumeData276 = read.csv("deliverables276/consume_loadings.csv", header=T, skip=1)
dim(consumeData276)


myPlot <- function(fb_number, disturbance, columnName){
  
  disturbanceNum <- substring(disturbance, 1, 1)
  
  baselineData284 <- consumeBaselineData284[consumeBaselineData284$fuelbed_number == fb_number, c('fuelbed_number', columnName, 'filename')]
  baselineData276 <- consumeBaselineData276[consumeBaselineData276$fuelbed_number == fb_number, c('fuelbed_number', columnName, 'filename')]
  
#  bdtest <- paste(fb_number, c(1,2,3,4,5), sep="_")
  bdtest <- paste(fb_number, disturbanceNum, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  fb_data284 <- consumeData284[consumeData284$fuelbed_number %in% bdtest, c('fuelbed_number', columnName, 'filename')]
  prefix284 <- substr(fb_data284$fuelbed_number, 0, nchar(fb_number) + 3)
  timeStep284 <- substr(fb_data284$fuelbed_number, nchar(fb_number) + 4, nchar(fb_number) + 4)

  fb_data276 <- consumeData276[consumeData276$fuelbed_number %in% bdtest, c('fuelbed_number', columnName, 'filename')]
  prefix276 <- substr(fb_data276$fuelbed_number, 0, nchar(fb_number) + 3)
  timeStep276 <- substr(fb_data276$fuelbed_number, nchar(fb_number) + 4, nchar(fb_number) + 4)
    
  fb_data284$Prefix <- prefix284
  fb_data284$TimeStep <- as.numeric(timeStep284)

  fb_data276$Prefix <- prefix276
  fb_data276$TimeStep <- as.numeric(timeStep276)
  
  baselineDataExpanded284 <- baselineData284[rep(row.names(baselineData284), length(unique(fb_data284$Prefix))), 1:3]
  baselineDataExpanded284$Prefix <- unique(fb_data284$Prefix)
  baselineDataExpanded284$TimeStep <- rep(0, length(unique(fb_data284$Prefix)))

  baselineDataExpanded276 <- baselineData276[rep(row.names(baselineData276), length(unique(fb_data276$Prefix))), 1:3]
  baselineDataExpanded276$Prefix <- unique(fb_data276$Prefix)
  baselineDataExpanded276$TimeStep <- rep(0, length(unique(fb_data276$Prefix)))
  
  combinedData284 <- rbind(fb_data284, baselineDataExpanded284)
  combinedData276 <- rbind(fb_data276, baselineDataExpanded276)
  
  mygraph284 <- ggplot(data = combinedData284, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph284 <- mygraph284 + guides(colour=guide_legend(title="Disturbance"))
  mygraph284 <- mygraph284 + ggtitle(paste(combinedData284$filename[1], "New Calculations (FCCS build 284)", sep=" ")) + xlim(0,3)

  mygraph276 <- ggplot(data = combinedData276, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph276 <- mygraph276 + guides(colour=guide_legend(title="Disturbance"))
  mygraph276 <- mygraph276 + ggtitle(paste(combinedData276$filename[1], "Original Calculations (FCCS build 276)", sep=" ")) + xlim(0,3)
  
  grid.arrange(mygraph276, mygraph284, nrow=2)
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(consumeBaselineData284$fuelbed_number, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(consumeBaselineData284), as.character)))

