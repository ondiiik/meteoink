from ui import UiFrame, Vect as V, BLACK, WHITE, BLUE


class UiRain(UiFrame):
    def draw(self, ui):
        # Pre-calculates some range values and draw icons bar
        forecast = ui.forecast.forecast
        cnt = len(forecast)
        cmax = cnt - 1
        block = ui.canvas.dim.x / cnt

        ui.canvas.hline(V(0, self.dim.y - 1), self.dim.x - 1, BLACK)

        for i in range(cnt):
            xx = int(block * i)
            weather = forecast[i]

            # Draw rain chart
            p = max(weather.rain, weather.snow)

            if weather.rain > 0 or weather.snow > 0:
                r = int(p * 12)
                q = self.dim.y // 4
                for h in (q, q * 2, q * 3):
                    if r > h:
                        r = h + (r - h) // 2
                v = V(xx - int(block // 2) + 1, self.dim.y - r - 1)
                d = V(int(block) - 2, r)

                if weather.rain > 0:
                    ui.canvas.fill_rect(v, d, BLUE)
                else:
                    ui.canvas.trect(v, d, BLUE)
                ui.canvas.rect(v, d, BLACK)

            # Type rain text
            if (i > 0) and (i < cmax):
                f0 = forecast[i - 1]
                f1 = forecast[i + 1]
                if (max(f0.rain, f0.snow) < p) and (p > max(f1.rain, f1.snow)):
                    ui.text_center(10, '%.1f' % p, V(xx, self.dim.y - 2), BLACK, WHITE)
