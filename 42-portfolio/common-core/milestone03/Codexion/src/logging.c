/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   logging.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:50 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	append_number(char *buffer, int *length, t_ticket value)
{
	char	digits[20];
	int		count;

	count = 0;
	while (value >= 10)
	{
		digits[count++] = '0' + value % 10;
		value /= 10;
	}
	digits[count++] = '0' + value;
	while (count > 0)
		buffer[(*length)++] = digits[--count];
}

static int	emit_line(t_coder *coder, const char *message, t_time at)
{
	char	buffer[128];
	int		length;
	int		index;

	if (strlen(message) > sizeof(buffer) - 43)
		return (coder_error(coder, "log: message too long", EOVERFLOW));
	length = 0;
	append_number(buffer, &length, (at - coder->sim->start) / 1000);
	buffer[length++] = ' ';
	append_number(buffer, &length, coder->id);
	buffer[length++] = ' ';
	index = 0;
	while (message[index])
		buffer[length++] = message[index++];
	buffer[length++] = '\n';
	if (!write_all(STDOUT_FILENO, buffer, length))
		return (coder_error(coder, "write(stdout)", errno));
	return (1);
}

void	log_state(t_coder *coder, const char *message, t_time at)
{
	int	result;

	if (!state_log_valid(coder, message, at))
		return ;
	result = pthread_mutex_lock(&coder->sim->log_lock);
	if (result)
	{
		coder_error(coder, "pthread_mutex_lock(log)", result);
		return ;
	}
	if (emit_line(coder, message, at))
	{
		if (strcmp(message, "is debugging") == 0)
			coder->state = CODER_DEBUGGING;
		else if (strcmp(message, "is refactoring") == 0)
			coder->state = CODER_REFACTORING;
	}
	result = pthread_mutex_unlock(&coder->sim->log_lock);
	if (result)
		coder_error(coder, "pthread_mutex_unlock(log)", result);
}

void	log_compile(t_coder *coder, t_time at)
{
	int	result;

	if (!log_valid(coder, "is compiling", at))
		return ;
	result = pthread_mutex_lock(&coder->sim->log_lock);
	if (result)
	{
		coder_error(coder, "pthread_mutex_lock(log)", result);
		return ;
	}
	if (emit_line(coder, "has taken a dongle", at)
		&& emit_line(coder, "has taken a dongle", at))
		emit_line(coder, "is compiling", at);
	result = pthread_mutex_unlock(&coder->sim->log_lock);
	if (result)
		coder_error(coder, "pthread_mutex_unlock(log)", result);
}

void	log_burnout(t_sim *sim, int index, t_time at)
{
	int	result;

	if (!sim_valid(sim) || index < 0 || index >= sim->capacity)
	{
		sim_error(sim, "burnout log: invalid simulation/index", index);
		return ;
	}
	if (!log_valid(&sim->coders[index], "burned out", at))
		return ;
	result = pthread_mutex_lock(&sim->log_lock);
	if (result)
	{
		sim_error(sim, "pthread_mutex_lock(log)", result);
		return ;
	}
	emit_line(&sim->coders[index], "burned out", at);
	result = pthread_mutex_unlock(&sim->log_lock);
	if (result)
		sim_error(sim, "pthread_mutex_unlock(log)", result);
}
