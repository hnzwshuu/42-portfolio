NAME = push_swap
CC = cc
CFLAGS = -Wall -Wextra -Werror
SRCS =	ft_bench.c \
		ft_disorder.c \
		ft_init_option.c \
		ft_init_stack_part1.c \
		ft_init_stack_part2.c \
		ft_libft_lst.c \
		ft_libft_put.c \
		ft_operation_push.c \
		ft_operation_reverse_rotate.c \
		ft_operation_rotate.c \
		ft_operation_swap.c \
		ft_operations_home.c \
		ft_sort_adaptive.c \
		ft_sort_complex_01.c \
		ft_sort_complex_02.c \
		ft_sort_medium_01.c \
		ft_sort_medium_02.c \
		ft_sort_mini.c \
		ft_sort_simple.c \
		main.c

OBJS = $(SRCS:.c=.o)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

all: $(NAME)

%.o: %.c
		$(CC) $(CFLAGS) -c $< -o $@

clean:
		rm -f $(OBJS)

fclean: clean
		rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
