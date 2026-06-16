import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MasterChild } from './master-child';

describe('MasterChild', () => {
  let component: MasterChild;
  let fixture: ComponentFixture<MasterChild>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MasterChild],
    }).compileComponents();

    fixture = TestBed.createComponent(MasterChild);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
