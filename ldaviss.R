ldavis_inputs = function(country)
{
	library(LDAvis)
	
	pi <- read.csv(paste("/Users/abbystevens/BigDataRenaissance/big-data-renaissance/csvisualations/", country, "Phi.csv", sep=""))
	phi<- data.matrix(subset(pi, select=-X))
	
	tok <- read.csv(paste("/Users/abbystevens/BigDataRenaissance/big-data-renaissance/csvisualations/", country, "Tokens.csv", sep=""))
	tokens <- data.matrix(tok$X)
	
	fre <- read.csv(paste("/Users/abbystevens/BigDataRenaissance/big-data-renaissance/csvisualations/", country, "Freqs.csv", sep=""))
	freq <- data.matrix(fre$X0)
	
	probs = rep(.1, 10)
	
	z<- check.inputs(K=10, W = length(tokens), phi=phi, token.frequency=freq, vocab=tokens, topic.proportion = probs)

	return(z)
}