import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrokerSettings } from './broker-settings';

describe('BrokerSettings', () => {
  let component: BrokerSettings;
  let fixture: ComponentFixture<BrokerSettings>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BrokerSettings],
    }).compileComponents();

    fixture = TestBed.createComponent(BrokerSettings);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
