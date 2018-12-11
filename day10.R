# AoC 2018 Day 10: The stars align
library(tidyverse)
# devtools::install_github('thomasp85/gganimate')
# devtools::install_github("r-rust/gifski")
# install.packages("transformr")
library(gganimate)

test_input <- "position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"

# input is a string vector of positions and speeds
parse_input <- function(input) {
  pos_and_speeds <- input %>% 
    read_lines() %>% 
    str_extract_all("-?\\d+", simplify=TRUE) %>% 
    as_tibble() %>% 
    map_dfr(as.integer)
  colnames(pos_and_speeds) <- c("x", "y", "vx", "vy")
  list(select(pos_and_speeds, "x", "y"),
       select(pos_and_speeds, "vx", "vy"))
}

pos_and_speeds_test <- parse_input(test_input)
pos_test <-  pos_and_speeds_test[[1]]
speeds_test <- pos_and_speeds_test[[2]]

plot_time <- function(pos_and_speeds, times) {
  pos <- pos_and_speeds[[1]]
  speeds <- pos_and_speeds[[2]]
  names(times) <- times  # for the .id
  times %>% 
    map_dfr(~pos + .x * speeds, .id = "time") %>% 
    mutate(time = as.integer(time)) %>% 
    ggplot(aes(x, y)) +
    geom_point() +
    coord_equal() +
    theme_minimal() +
    labs(title = "t={closest_state}") +
    transition_states(time, 
                      transition_length = 3,
                      state_length = 2)
}

parse_input(test_input) %>% 
  plot_time(1:5)

# With trial and error
parse_input("day10_input.txt") %>% 
  plot_time(seq(10510, 10520, by = 1))

pos_and_speeds <- parse_input("day10_input.txt")
pos <- pos_and_speeds[[1]]
speeds <-  pos_and_speeds[[2]]

# We need to flip the y value to plot it in the good order
(pos + 10519 * speeds) %>%
  mutate(y=-y) %>% 
  ggplot(aes(x, y)) +
  geom_point() + 
  coord_equal()
