/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:19 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	absolute_timeout(t_sim *sim, t_time deadline,
		struct timespec *absolute)
{
	t_time	remaining;
	t_time	nanoseconds;
	t_time	seconds;
	t_time	now;

	now = now_us(sim);
	if (now < 0 || deadline < 0)
		return (sim_error(sim, "wait: invalid deadline or clock", ERANGE));
	remaining = deadline - now;
	if (remaining <= 0)
		return (-1);
	if (remaining > 10000)
		remaining = 10000;
	if (!read_time(sim, CLOCK_REALTIME, absolute))
		return (0);
	nanoseconds = absolute->tv_nsec + remaining * 1000;
	seconds = (t_time)absolute->tv_sec + nanoseconds / 1000000000;
	if ((t_time)(time_t)seconds != seconds)
		return (sim_error(sim, "wait: time_t overflow", ERANGE));
	absolute->tv_sec = (time_t)seconds;
	absolute->tv_nsec = nanoseconds % 1000000000;
	return (1);
}

void	wait_event(t_sim *sim)
{
	if (!sim)
		sim_error(sim, "event wait: invalid simulation", EINVAL);
	else
		wait_until(sim, &sim->event, deadline_after(sim, now_us(sim), 10000));
}

void	wait_until(t_sim *sim, pthread_cond_t *cond, t_time deadline)
{
	struct timespec	absolute;
	int				result;

	if (!sim_valid(sim) || (cond != &sim->event && cond != &sim->watch))
	{
		sim_error(sim, "condition wait: invalid context", EINVAL);
		return ;
	}
	if (sim->stopped || absolute_timeout(sim, deadline, &absolute) != 1)
		return ;
	result = pthread_cond_timedwait(cond, &sim->lock, &absolute);
	if (result != 0 && result != ETIMEDOUT)
		sim_error(sim, "pthread_cond_timedwait", result);
}

int	pause_until(t_sim *sim, t_time deadline)
{
	if (deadline < 0)
		return (sim_error(sim, "phase wait: negative deadline", ERANGE));
	while (sim_live(sim) && now_us(sim) < deadline)
		wait_until(sim, &sim->event, deadline);
	return (sim_live(sim));
}
