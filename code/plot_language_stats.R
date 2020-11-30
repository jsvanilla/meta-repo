library(here)
library(RColorBrewer)
library(tidyverse)
theme_set(theme_classic())
update_geom_defaults("bar", list(fill = RColorBrewer::brewer.pal(n=9,name="GnBu")[9]))
theme_update(axis.text.x = element_text(angle = 45, hjust = 1))

plot_bar <- function(data,
                     x_col = language,
                     y_col = total_bytes,
                     xlab_str = '',
                     ylab_str = '',
                     title_str = '') {
    
    return( data %>%
        ggplot2::ggplot(aes(x = {{ x_col }}, 
                            y = {{ y_col }}, 
                            label = {{ y_col }})) +
            geom_bar(stat="identity")+
            geom_text(aes(label={{ y_col }}), vjust = -0.4, size = 3) +
            scale_y_continuous(
                breaks = c(100000, 250000, 500000, 750000, 1000000),
                labels = c('100k', '250k', '500k', '750k', '1mil')
            ) +
            xlab(xlab_str) +
            ylab(ylab_str) +
            #coord_flip() +
            ggtitle(title_str)
    )
}
write_plot <- function(plot,
                           filename = NULL,
                           aspect_ratio = 4 / 3,
                           height = 6,
                           width = NULL,
                           units = "in") {
        
        if (is.null(width)) {
            width <- height * aspect_ratio
        }
    if (!is.null(filename)) {
        ggsave(
            here::here("figures", filename),
            plot = plot,
            height = height,
            width = width,
            units = units
        )
    }
}


sum_lang_data <- function(data) {
    return(
        data %>%
            filter(!(
                repo_name %in% c("caret",
                                 "CluMSID",
                                 'schlosslab.github.io',
                                 "mothur.github.io",
                                 '2020-01-06-UMich-WISE',
                                 '2021-01-11-UMich-WISE')
            )) %>%
            filter(!(
                repo_owner_name %in% c("JMAStough",
                                       "akhagan",
                                       "mothur")
            )) %>%
            group_by(language) %>%
            summarize(
                total_bytes = sum(language_repo_bytes),
                repo_count = n()
            )
    )
}


data_raw <-
    readr::read_csv(here::here("data", "repo_languages.csv"))
data_sum <- sum_lang_data(data_raw) %>%
    filter(!(language %in% c("HTML", "CSS", "Limbo"))) %>%
    mutate(language = reorder(language, -total_bytes))

# all bytes
data_sum %>%
    plot_bar(
        x_col = language,
        y_col = total_bytes,
        ylab_str = "bytes of code",
        title_str = "My languages by bytes of code on GitHub"
    ) %>%
    write_plot(filename = "language_all_bytes.png")

# bytes top 6
data_sum %>% top_n(6, total_bytes) %>%
    plot_bar(
        x_col = language,
        y_col = total_bytes,
        ylab_str = "bytes of code",
        title_str = "My top languages on GitHub"
    ) %>% write_plot(filename = "language_all_bytes_n6.png",
                     height = 4,
                     width = 4)

# all repos
data_sum %>%
    mutate(language = reorder(language, -repo_count)) %>%
    plot_bar(
        x_col = language,
        y_col = repo_count,
        ylab_str = "# of repos",
        title_str = "My languages by presence in GitHub repositories"
    ) %>% 
    write_plot(filename = "language_all_repos.png")
