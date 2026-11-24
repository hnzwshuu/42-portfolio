/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: soarai <soarai@student.42tokyo.jp>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/15 16:27:50 by soarai            #+#    #+#             */
/*   Updated: 2026/05/27 20:19:11 by soarai           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <limits.h>
# include <stdbool.h>
# include <stdio.h>
# include <stdlib.h>
# include <unistd.h>

# define ERROR -1
# define SIMPLE 0
# define MEDIUM 1
# define COMPLEX 2
# define ADAPTIVE 3
# define BENCH 4
# define SA 0
# define SB 1
# define SS 2
# define PA 3
# define PB 4
# define RA 5
# define RB 6
# define RR 7
# define RRA 8
# define RRB 9
# define RRR 10

# define A 0
# define B 1

typedef struct s_stack
{
	long			content;
	struct s_stack	*next;
}					t_stack;

// bench.c
void				print_disorder(long disorder);
void				print_strategy(ssize_t strategy, long disorder);
void				print_counter(int *counter);
void				print_counter_elements(int *counter, int i);
void				print_operations(int element);
// disorder.c
long				measure_disorder(t_stack **stack);
void				init_operation_counter(int *counter);
// init_option.c
ssize_t				define_option(char **argv);
ssize_t				define_strategy(char *strategy);
ssize_t				match_strategy(char *strategy, char *target, ssize_t value);
ssize_t				hyphen_or_digit(char *strategy);
// init_stack_part1.c
t_stack				**malloc_stack(char **argv, t_stack **stack);
ssize_t				measure_stack(char **argv);
ssize_t				pos_dig_s(char *target);
bool				check_digit(char *strnum);
// init_stack_part2.c
t_stack				**make_stack(char **argv, t_stack **stack, ssize_t size,
						long *memories);
long				ft_atol(const char *nptr);
bool				check_dupmem(long *memories, size_t bp);
t_stack				**malloc_dps(void);
// libft_lst.c
t_stack				*ft_lstnew(long content);
void				ft_lstadd_front(t_stack **lst, t_stack *new, size_t sp);
void				ft_lstadd_back(t_stack **lst, t_stack *new, size_t sp);
t_stack				**ft_lstclear(t_stack **lst, size_t sp);
int					ft_lstsize(t_stack *stack);
// libft_put.c
int					ft_strlen(char *str);
void				ft_putnbr_fd(int n, int fd);
void				ft_putendl_fd(char *s, int fd);
// main.c
ssize_t				solve_cmdline(char **argv, t_stack **stack);
void				solve_sort(t_stack **stack, ssize_t strategy, int *counter);
void				solve_benchmark(ssize_t strategy, long disorder,
						int *counter);
void				solve_stack_mini(t_stack **stack, int *counter);
// operation_push.c
void				pa(t_stack **stack);
void				pb(t_stack **stack);
// operation_reverse_rotate.c
t_stack				*lstbeforelast(t_stack **stack, size_t sp);
void				rra(t_stack **stack);
void				rrb(t_stack **stack);
void				rrr(t_stack **stack);
// operation_rotate.c
t_stack				*lstlast(t_stack **stack, size_t sp);
void				ra(t_stack **stack);
void				rb(t_stack **stack);
void				rr(t_stack **stack);
// operation_swap.c
void				sa(t_stack **stack);
void				sb(t_stack **stack);
void				ss(t_stack **stack);
// operation_home.c
void				operations(t_stack **stack, char *operation, int *counter);
void				operations_s(t_stack **stack, char *operation,
						int *counter);
void				operations_p(t_stack **stack, char *operation,
						int *counter);
void				operations_r(t_stack **stack, char *operation,
						int *counter);
void				operations_rr(t_stack **stack, char *operation,
						int *counter);
// sort_adaptive.c
void				sort_adaptive(t_stack **stack, int *counter, long disorder);
// sort_complex_01.c
void				sort_complex(t_stack **stack, int *counter);
void				max_min_digit(t_stack **stack, long *min_max);
void				sort_place(t_stack **stack, size_t place, int *counter);
bool				match_target(size_t rank, size_t place, int target);
// sort_complex_02.c
size_t				make_place(size_t place);
// sort_medium_01.c
void				sort_medium(t_stack **stack, int *counter);
size_t				int_sqrt(size_t size);
size_t				value_rank(t_stack **stack, long value);
void				push_chunks_to_b(t_stack **stack, int *counter);
void				move_mex_to_a(t_stack **stack, int *counter);
// sort_medium_02.c
size_t				max_position(t_stack *stack);
// sort_mini.c
void				sort_under_three(t_stack **stack, int *counter);
void				sort_under_five(t_stack **stack, int *counter);
// sort_simple.c
void				sort_simple(t_stack **stack, int *counter);
size_t				stack_size(t_stack *stack);
int					is_sorted(t_stack **stack);
void				move_min_to_top(t_stack **stack, int *counter);

#endif
