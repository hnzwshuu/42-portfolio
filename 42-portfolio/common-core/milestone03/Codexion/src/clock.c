/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clock.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:04:53 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	read_time(t_sim *sim, clockid_t id, struct timespec *value)
{
	const char	*operation;

	if (!value || (id != CLOCK_MONOTONIC && id != CLOCK_REALTIME))
		return (sim_error(sim, "clock: invalid argument", EINVAL));
	operation = "clock_gettime(monotonic)";
	if (id == CLOCK_REALTIME)
		operation = "clock_gettime(realtime)";
	if (clock_gettime(id, value) != 0)
		return (sim_error(sim, operation, errno));
	if (value->tv_sec < 0 || value->tv_nsec < 0
		|| value->tv_nsec >= 1000000000
		|| (t_ticket)value->tv_sec > (LLONG_MAX - 999999) / 1000000)
		return (sim_error(sim, "clock: invalid result", ERANGE));
	return (1);
}

t_time	now_us(t_sim *sim)
{
	struct timespec	now;

	if (!read_time(sim, CLOCK_MONOTONIC, &now))
		return (-1);
	return ((t_time)now.tv_sec * 1000000 + now.tv_nsec / 1000);
}

t_time	deadline_after(t_sim *sim, t_time base, t_time duration)
{
	if (base < 0 || duration < 0 || duration > LLONG_MAX - base)
	{
		sim_error(sim, "time: invalid value or deadline overflow", ERANGE);
		return (-1);
	}
	return (base + duration);
}
