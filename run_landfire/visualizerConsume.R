library(ggplot2) 
library(manipulate)

consumeBaselineData = read.csv("baseline/consume_loadings.csv", header=T, skip=1)
dim(consumeBaselineData)

consumeData = read.csv("deliverables/consume_loadings.csv", header=T, skip=1)
dim(consumeData)

myPlot <- function(fb_number, disturbance, columnName){
  
  disturbanceNum <- substring(disturbance, 1, 1)
  
  baselineData <- consumeBaselineData[consumeBaselineData$fuelbed_number == fb_number, c('fuelbed_number', columnName, 'filename')]
  
#  bdtest <- paste(fb_number, c(1,2,3,4,5), sep="_")
  bdtest <- paste(fb_number, disturbanceNum, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  fb_data <- consumeData[consumeData$fuelbed_number %in% bdtest, c('fuelbed_number', columnName, 'filename')]
  prefix <- substr(fb_data$fuelbed_number, 0, nchar(fb_number) + 3)
  timeStep <- substr(fb_data$fuelbed_number, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  fb_data$Prefix <- prefix
  fb_data$TimeStep <- as.numeric(timeStep)
  
  baselineDataExpanded <- baselineData[rep(row.names(baselineData), length(unique(fb_data$Prefix))), 1:3]
  baselineDataExpanded$Prefix <- unique(fb_data$Prefix)
  baselineDataExpanded$TimeStep <- rep(0, length(unique(fb_data$Prefix)))

  combinedData <- rbind(fb_data, baselineDataExpanded)

  mygraph <- ggplot(data = combinedData, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph <- mygraph + guides(colour=guide_legend(title="Disturbance"))
  mygraph + ggtitle(combinedData$filename[1]) + xlim(0,3)
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(consumeBaselineData$fuelbed_number, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(consumeBaselineData), as.character)))

