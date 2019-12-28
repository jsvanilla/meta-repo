library(here)
library(RColorBrewer)
library(tidyverse)
theme_set(theme_classic())
update_geom_defaults("bar", list(fill = RColorBrewer::brewer.pal(n=9,name="GnBu")[9]))
theme_update(axis.text.x = element_text(angle = 45, hjust = 1))

plot_bar <- function(data, x_str, y_str, xlab_str, ylab_str, title_str, filename) {
    plot <- data %>%
        ggplot2::ggplot(aes_string(x=x_str, y=y_str, label=y_str)) +
        geom_bar(stat="identity")+#, fill="#0868AC") +
        geom_text(aes_string(label=y_str), vjust=-0.5, size=3) +
        xlab(xlab_str) +
        ylab(ylab_str) +
        ggtitle(title_str)
    aspect_ratio <- 4/3
    height <- 5
    width <- height * aspect_ratio
    ggsave(here::here("figures", filename), height=height, width=width, units="in")
    return(plot)
}

sum_lang_data <- function(data) {
    return(data %>%
               filter(!(repo_name %in% c("ML_pipeline_microbiome"))) %>%
               filter(!(repo_owner_name %in% c("JMAStough", "akhagan"))) %>%
               group_by(language) %>%
               summarize(total_bytes=sum(language_repo_bytes),
                         repo_count=n())
    )
}

data_raw <- readr::read_csv(here::here("data", "repo_languages.csv"))
data <- sum_lang_data(data_raw) %>%
    filter(!(language %in% c("HTML", "CSS", "Limbo")))

plot_all_bytes <- plot_bar(data %>% 
                               mutate(language=reorder(language, -total_bytes)), 
                           "language", "total_bytes", "language", "bytes of code", 
                           "My languages by bytes of code on GitHub", "language_all_bytes.png")

plot_bytes_7 <- plot_bar(data %>% 
                             mutate(language=reorder(language, -total_bytes)) %>% 
                             top_n(7, total_bytes), 
                         "language", "total_bytes","language", "bytes of code", 
                         "My top 7 languages by bytes of code on GitHub", "language_all_bytes_n7.png")

plot_all_repos <- plot_bar(data %>% 
                               mutate(language=reorder(language, -repo_count)),
                           "language", "repo_count","language", "# of repos", 
                           "My languages by presence in GitHub repositories", "language_all_repos.png")
