## Compare the MCMC samples from the GUI and the INCAWrapper
## NB this file should be run from the root of the INCAWrapper repository
## Use following command to run this script:
## `Rscript 'docs/examples/Literature data/simple model/compare_mcmc_samples.R'`

# Install the Hotelling package if it is not already installed
if (!requireNamespace("Hotelling", quietly = TRUE)) {
    print("Please install the Hotelling package on your system")
}
library(Hotelling)

# Load the MCMC samples
samples_from_gui <- as.matrix(read.csv("docs/examples/Literature data/simple model/simulated_data/simple_model_gui_mcmc_results.csv", header = TRUE))
samples_from_wrapper <- as.matrix(read.csv("docs/examples/Literature data/simple model/simulated_data/simple_model_incawrapper_mcmc_results.csv", header = TRUE))

colnames(samples_from_gui) <- colnames(samples_from_wrapper)

# Free fluxes
free_fluxes <- c("R2.net", "R2.exch", "R3")
print("Using only free fluxes for comparison. The free fluxes are:")
print(free_fluxes)

samples_from_gui_free <- samples_from_gui[, colnames(samples_from_gui) %in% free_fluxes]
samples_from_wrapper_free <- samples_from_wrapper[, colnames(samples_from_wrapper) %in% free_fluxes]

# Compare the MCMC samples using hotelling's T^2 test
out <- hotelling.test(
    x = samples_from_gui_free,
    y = samples_from_wrapper_free, shrinkage = FALSE,
    var.equal = TRUE,
    perm = TRUE,
    B = 1000000,
)

print("Results of the Hotelling's T^2 test:")
print(out)

# Extract main results
p_value <- out$pval
degree_of_freedom <- out$stats$df
n_permutations <- length(out$results)

# Create data frame
results <- t(data.frame(
    p_value = p_value,
    degree_of_freedom_1 = degree_of_freedom[1],
    degree_of_freedom_2 = degree_of_freedom[2],
    n_permutations = n_permutations
))
colnames(results) <- c("value")

print(results)
# store the results in a txt file
write.table(results, file = "docs/examples/Literature data/simple model/simulated_data/hotelling_test_results.txt", row.names = TRUE, col.names = TRUE)
