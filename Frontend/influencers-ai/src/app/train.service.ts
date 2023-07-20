import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TrainService {
  private token: string = sessionStorage.getItem('token') || '';
  private baseUrl: string = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  addTranscript(transcript: string): Observable<any> {
    const url = `${this.baseUrl}/train/add-transcript`;
    const body = {
      transcript,
    };
    return this.http.post(url, body, {
      headers: {
        Authorization: `${this.token}`,
      },
    });
  }

  getTranscripts(): Observable<any> {
    const url = `${this.baseUrl}/train/get-transcripts`;
    return this.http.get(url, {
      headers: {
        Authorization: `${this.token}`,
      },
    });
  }

  addQnA(question: string, answer: string): Observable<any> {
    const url = `${this.baseUrl}/train/add-qna`;
    const body = {
      question,
      answer,
    };
    return this.http.post(url, body, {
      headers: {
        Authorization: `${this.token}`,
      },
    });
  }

  getQnAs(): Observable<any> {
    const url = `${this.baseUrl}/train/get-qnas`;
    return this.http.get(url, {
      headers: {
        Authorization: `${this.token}`,
      },
    });
  }

  train(): Observable<any> {
    const url = `${this.baseUrl}/train`;
    return this.http.get(url, {
      headers: {
        Authorization: `${this.token}`,
      },
    });
  }
}
