library(ggplot2) 
library(manipulate)

fccsData = read.csv("deliverables/fccs_summary.csv", header=T)
dim(fccsData)

fccsBaselineData = read.csv("baseline/fccs_summary.csv", header=T)
dim(fccsBaselineData)

myPlot <- function(fb_number, disturbance, columnName){
  
  disturbance <- substring(disturbance, 1, 1)
  
  baselineData <- fccsBaselineData[fccsBaselineData$Fuelbed_number == fb_number, c('Fuelbed_number', columnName, 'Fuelbed_name')]
  
#  bdtest <- paste(fb_number, c(1,2,3,4,5), sep="_")
  bdtest <- paste(fb_number, disturbance, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  fb_data <- fccsData[fccsData$Fuelbed_number %in% bdtest, c('Fuelbed_number', columnName, 'Fuelbed_name')]
  prefix <- substr(fb_data$Fuelbed_number, 0, nchar(fb_number) + 3)
  timeStep <- substr(fb_data$Fuelbed_number, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  fb_data$Prefix <- prefix
  fb_data$TimeStep <- as.numeric(timeStep)
  
  baselineDataExpanded <- baselineData[rep(row.names(baselineData), length(unique(fb_data$Prefix))), 1:3]
  baselineDataExpanded$Prefix <- unique(fb_data$Prefix)
  baselineDataExpanded$TimeStep <- rep(0, length(unique(fb_data$Prefix)))
  baselineDataExpanded
  
  combinedData <- rbind(fb_data, baselineDataExpanded)

  mygraph <- ggplot(data = combinedData, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph + ggtitle(combinedData$Fuelbed_name[1]) + xlim(0,3)
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(fccsBaselineData$Fuelbed_number, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(fccsBaselineData), as.character)))

