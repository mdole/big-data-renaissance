ldavis_inputs = function(phifile, tokenfile, freqfile)
{
	library(LDAvis)
	
	pi <- read.csv(phifile)
	phi<- data.matrix(subset(pi, select=-X))
	
	tok <- read.csv(tokenfile)
	tokens <- data.matrix(tok$X)
	
	fre <- read.csv(freqfile)
	freq <- data.matrix(fre$X0)
	
	probs = rep(.1, 10)
	
	z<- check.inputs(K=10, W = length(tokens), phi=phi, token.frequency=freq, vocab=tokens, topic.proportion = probs)

	return(z)
}