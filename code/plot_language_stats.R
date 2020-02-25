library(here)
library(RColorBrewer)
library(tidyverse)
theme_set(theme_classic())
update_geom_defaults("bar", list(fill = RColorBrewer::brewer.pal(n=9,name="GnBu")[9]))
theme_update(axis.text.x = element_text(angle = 45, hjust = 1))

plot_bar <- function(data, x_col = language, y_col = total_bytes, 
                     xlab_str ='', ylab_str='', title_str='', filename = NULL,
                     aspect_ratio = 4/3, height = 6, width = NULL, units = "in") {
    plot <- data %>%
        ggplot2::ggplot(aes(x = {{ x_col }}, 
                            y = {{ y_col }}, 
                            label = {{ y_col }})) +
        geom_bar(stat="identity")+#, fill="#0868AC") +
        geom_text(aes(label={{ y_col }}), vjust=-0.5, size=3) +
        xlab(xlab_str) +
        ylab(ylab_str) +
        ggtitle(title_str)
    
    if (is.null(width)) {
        width <- height * aspect_ratio
    }
    if (!is.null(filename)) {
        ggsave(here::here("figures", filename),
               height=height, width=width, units=units)
    }
    return(plot)
}

sum_lang_data <- function(data) {
    return(data %>%
               filter(!(repo_name %in% c("ML_pipeline_microbiome", 
                                         "caret", 
                                         "CluMSID"))) %>%
               filter(!(repo_owner_name %in% c("JMAStough", 
                                               "akhagan"))) %>%
               group_by(language) %>%
               summarize(total_bytes=sum(language_repo_bytes),
                         repo_count=n())
    )
}

data_raw <- readr::read_csv(here::here("data", "repo_languages.csv"))
data_sum <- sum_lang_data(data_raw) %>%
    filter(!(language %in% c("HTML", "CSS", "Limbo"))) %>% 
    mutate(language=reorder(language, -total_bytes))

plot_all_bytes <- data_sum %>% plot_bar( 
                           x_col = language, y_col = total_bytes, 
                           ylab_str = "bytes of code", 
                           title_str = "My languages by bytes of code on GitHub", 
                           filename = "language_all_bytes.png")

plot_bytes_5 <- plot_bar(data_sum %>% top_n(5, total_bytes), 
                         x_col = language, y_col = total_bytes, 
                         ylab_str = "bytes of code", 
                         title_str = "My top languages on GitHub", 
                         filename = "language_all_bytes_n5.png", 
                         height = 4, width = 4)

plot_all_repos <- plot_bar(data_sum %>% 
                               mutate(language=reorder(language, -repo_count)),
                           x_col = language, y_col = repo_count,
                           ylab_str = "# of repos", 
                           title_str = "My languages by presence in GitHub repositories", 
                           filename = "language_all_repos.png")

