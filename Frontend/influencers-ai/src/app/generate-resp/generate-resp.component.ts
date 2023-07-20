import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { TrainService } from '../train.service';

@Component({
  selector: 'app-generate-resp',
  templateUrl: './generate-resp.component.html',
  styleUrls: ['./generate-resp.component.scss'],
})
export class GenerateRespComponent implements OnInit {
  private influencer: any = {};

  protected fetchedQnAs: any = [];

  constructor(
    private apiAuthserv: AuthService,
    private apiTrainServ: TrainService
  ) {}

  ngOnInit(): void {
    this.apiAuthserv.getInfluencer().subscribe(
      (res) => {
        if (res.status == 'success') {
          this.influencer = res.data;
          sessionStorage.setItem('influencer_name', this.influencer.name);
        } else {
          window.location.href = '/home';
        }
      },
      (err) => {
        window.location.href = '/home';
      }
    );

    this.apiTrainServ.getQnAs().subscribe(
      (res) => {
        if (res.status == 'success') {
          this.fetchedQnAs = [
            {
              question: 'How are you?',
              answer: 'I am fine',
            },
          ];
        } else {
          console.log(res);
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }
}
