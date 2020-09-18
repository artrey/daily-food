import csv
from functools import partial

from django.core.management.base import BaseCommand

from ...models import WakingDay, FoodItem


class Command(BaseCommand):
    help = 'Export dairy data to csv'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
        )
        parser.add_argument(
            '-o', '--output',
            type=str,
            help='file output, if None then stdout'
        )

    def handle(self, username, *args, **options):
        write_csv = partial(self.write_csv, username)

        output = options.get('output')
        if output:
            with open(output, 'w', encoding='utf-8') as fd:
                write_csv(fd)
        else:
            write_csv(self.stdout)

    def write_csv(self, username, stream):
        writer = csv.writer(stream, lineterminator='\n')

        writer.writerow((
            'Время', 'Продукт', 'Масса', 'К', 'Б', 'Ж', 'У',
        ))

        for day in WakingDay.objects.filter(
            user__username=username
        ).order_by('day'):
            writer.writerow((day,))
            for ea in day.eating_actions.order_by('time_moment'):
                tm = ea.time_moment.astimezone().time().strftime('%H:%M')
                for idx, fi in enumerate(ea.food_items.all()):
                    writer.writerow((
                        '' if idx else tm, fi.name, fi.mass,
                        fi.energy, fi.carbs, fi.fats, fi.proteins,
                    ))
                writer.writerow(('Примечание', ea.comment,))

            writer.writerow(('Общее примечание', day.comment,))
            writer.writerow([])
