import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (isLoading) {
      <div class="spinner-overlay">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
    }
  `, templateUrl: './loading-spinner.html',
  styleUrl: './loading-spinner.scss',
  styles: ['.spinner-overlay { position: fixed; inset: 0; display: grid; place-items: center; background: rgba(255,255,255,0.7); z-index: 9999; }']
},
)
export class LoadingSpinner {
  @Input() isLoading = false;
}
