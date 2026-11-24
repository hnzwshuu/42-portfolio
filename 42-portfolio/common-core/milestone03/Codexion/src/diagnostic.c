/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   diagnostic.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:29 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	boundary_error(const char *message, t_time value)
{
	if (!message)
		message = "invalid argument";
	fprintf(stderr, "Error: %s (value/code %lld)\n", message, value);
	return (0);
}
