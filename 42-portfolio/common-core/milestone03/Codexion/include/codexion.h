/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:04:47 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <errno.h>
# include <limits.h>
# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <time.h>
# include <unistd.h>

# define HEAP_CAPACITY 2
# define PAIR_WAIT -1
# define PAIR_GRANTED -2
# define PAIR_ERROR -3
# define SIM_EMPTY 0
# define SIM_READY 1
# define SIM_RUNNING 2
# define SIM_DONE 3
# define CODER_WAITING 0
# define CODER_COMPILING 1
# define CODER_DEBUGGING 2
# define CODER_REFACTORING 3
# define CODER_SINGLE 4

typedef long long			t_time;
typedef unsigned long long	t_ticket;
typedef struct s_coder		t_coder;
typedef struct s_sim		t_sim;

typedef struct s_config
{
	int		count;
	t_time	burnout;
	t_time	compile;
	t_time	debug;
	t_time	refactor;
	int		required;
	t_time	cooldown;
	int		edf;
}	t_config;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	t_coder			*heap[HEAP_CAPACITY];
	int				size;
	int				owner;
	t_time			ready_at;
}	t_dongle;

struct s_coder
{
	t_sim		*sim;
	pthread_t	thread;
	int			id;
	int			left;
	int			right;
	t_time		last_start;
	t_time		initial_delay;
	t_time		released_at;
	t_ticket	ticket;
	int			completed;
	int			finished;
	int			queued;
	int			state;
};

struct s_sim
{
	t_config		conf;
	t_dongle		*dongles;
	t_coder			*coders;
	pthread_mutex_t	lock;
	pthread_mutex_t	log_lock;
	pthread_cond_t	event;
	pthread_cond_t	watch;
	pthread_t		monitor;
	t_time			start;
	t_ticket		next_ticket;
	int				ready;
	int				stopped;
	int				failed;
	int				finished_count;
	int				initialized_dongles;
	int				sync_stage;
	int				created;
	int				monitor_created;
	int				capacity;
	int				phase;
	const char		*error;
	int				error_code;
};

int		parse_config(int argc, char **argv, t_config *conf);
int		config_valid(const t_config *conf);
int		sim_valid(t_sim *sim);
int		coder_valid(t_coder *coder);
int		coder_state_valid(t_coder *coder);
int		coder_error(t_coder *coder, const char *message, int code);
int		pair_valid(t_coder *coder);
int		pair_requested(t_coder *coder);
int		log_valid(t_coder *coder, const char *message, t_time at);
int		state_log_valid(t_coder *coder, const char *message, t_time at);
int		boundary_error(const char *message, t_time value);
int		record_error(t_sim *sim, const char *message, int code);
int		sim_error(t_sim *sim, const char *message, int code);
void	report_error(t_sim *sim);
int		sim_lock(t_sim *sim);
int		sim_unlock(t_sim *sim);
int		sim_notify(t_sim *sim, int watch);
int		sim_init(t_sim *sim, t_config *conf);
int		sim_destroy(t_sim *sim);
int		sim_run(t_sim *sim);
int		sim_join(t_sim *sim);
void	prepare_start(t_sim *sim);
t_time	initial_delay(t_config *conf, int index);
void	sim_stop(t_sim *sim);
int		sim_live(t_sim *sim);
int		sim_active(t_sim *sim);
int		expired_coder(t_sim *sim, t_time now);
int		wait_ready(t_sim *sim);
void	*monitor_main(void *arg);
void	*coder_main(void *arg);
void	coder_loop(t_coder *coder);
t_time	now_us(t_sim *sim);
int		read_time(t_sim *sim, clockid_t id, struct timespec *value);
t_time	deadline_after(t_sim *sim, t_time base, t_time duration);
void	wait_until(t_sim *sim, pthread_cond_t *cond, t_time deadline);
void	wait_event(t_sim *sim);
int		pause_until(t_sim *sim, t_time deadline);
int		request_before(t_coder *a, t_coder *b);
int		request_order(t_coder *a, t_coder *b);
int		request_valid(t_coder *coder);
int		heap_valid(t_dongle *dongle);
int		heap_can_push(t_dongle *dongle, t_coder *coder);
int		heap_accepts(t_dongle *dongle, t_coder *coder);
int		heap_push(t_dongle *dongle, t_coder *coder);
void	heap_insert(t_dongle *dongle, t_coder *coder);
t_coder	*heap_pop(t_dongle *dongle);
t_coder	*heap_remove(t_dongle *dongle);
int		pair_lock(t_coder *coder);
int		pair_lock_validated(t_coder *coder);
int		pair_unlock(t_coder *coder);
int		queue_request(t_coder *coder);
int		acquire_pair(t_coder *coder);
int		release_pair(t_coder *coder);
void	single_coder(t_coder *coder);
void	log_state(t_coder *coder, const char *message, t_time at);
void	log_compile(t_coder *coder, t_time at);
void	log_burnout(t_sim *sim, int index, t_time at);
void	write_error(const char *message);
int		write_all(int fd, const char *buffer, size_t length);

#endif
