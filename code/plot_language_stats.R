
library(here)
library(RColorBrewer)
library(tidyverse)
theme_set(theme_classic())
update_geom_defaults("bar", list(fill = RColorBrewer::brewer.pal(n=9,name="GnBu")[9]))
theme_update(axis.text.x = element_text(angle = 45, hjust = 1))
aspect_ratio <- 4/3
height <- 5
width <- height * aspect_ratio

data <- readr::read_csv(here::here("data", "repo_languages.csv")) %>%
    filter(!(language %in% c("HTML", "CSS")))

plot_all_bytes <- data %>%
    group_by(language) %>%
    summarize(total_bytes=sum(language_repo_bytes)) %>%
    ggplot2::ggplot(aes(x=reorder(language, -total_bytes), y=total_bytes, ladbel=total_bytes)) +
    geom_bar(stat="identity")+#, fill="#0868AC") +
    geom_text(aes(label=total_bytes), vjust=-0.5, size=3) +
    xlab("language") +
    ylab("bytes of code") +
    ggtitle("My languages by bytes of code on GitHub")
ggsave(here::here("figures", "language_all_bytes.svg"), height=height, width=width, units="in")

plot_bytes_7 <- data %>%
    group_by(language) %>%
    summarize(total_bytes=sum(language_repo_bytes)) %>%
    top_n(7, total_bytes) %>%
    ggplot2::ggplot(aes(x=reorder(language, -total_bytes), y=total_bytes, label=total_bytes)) +
    geom_bar(stat="identity")+#, fill="#0868AC") +
    geom_text(aes(label=total_bytes), vjust=-0.5, size=3) +
    xlab("language") +
    ylab("bytes of code") +
    ggtitle("My top 7 languages by bytes of code on GitHub")
ggsave(here::here("figures", "language_all_bytes_n7.svg"), height=height, width=width, units="in")

plot_all_repos <- data %>%
    group_by(language) %>%
    summarize(repo_count=n()) %>%
    ggplot2::ggplot(aes(x=reorder(language, -repo_count), y=repo_count, label=repo_count)) +
    geom_bar(stat="identity")+#, fill="#0868AC") +
    geom_text(aes(label=repo_count), vjust=-0.5, size=3) +
    xlab("language") +
    ylab("# of repos") +
    ggtitle("My languages by presence in GitHub repositories")
ggsave(here::here("figures", "language_all_repos.svg"), height=height, width=width, units="in")
